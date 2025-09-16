import bpy
import json
import os
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

class UDO_OT_export_blendshape(Operator, ExportHelper):
    """Export blendshape animations to JSON format for Unity"""
    bl_idname = "udo.export_blendshape"
    bl_label = "Export Blendshape Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    def execute(self, context):
        props = context.scene.animation_export_props
        obj = context.active_object
        
        # Validation
        if not obj:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
        
        if not obj.data.shape_keys:
            self.report({'ERROR'}, "Object has no shape keys")
            return {'CANCELLED'}
        
        # Get the action to export
        action = None
        if props.use_active_action:
            if obj.animation_data and obj.animation_data.action:
                action = obj.animation_data.action
            else:
                self.report({'ERROR'}, "No active action on object")
                return {'CANCELLED'}
        else:
            if props.selected_action != "NONE":
                action = bpy.data.actions.get(props.selected_action)
                if not action:
                    self.report({'ERROR'}, f"Action '{props.selected_action}' not found")
                    return {'CANCELLED'}
            else:
                self.report({'ERROR'}, "No action selected")
                return {'CANCELLED'}
        
        try:
            self.export_blendshape_animation(obj, action, self.filepath, props)
            self.report({'INFO'}, f"Exported blendshape animation to: {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
    
    def export_blendshape_animation(self, obj, action, filepath, props):
        """Core export functionality"""
        fps = bpy.context.scene.render.fps
        
        # Get frame range
        if props.use_frame_range:
            frame_start = props.frame_start
            frame_end = props.frame_end
        else:
            frame_start = int(action.frame_range[0])
            frame_end = int(action.frame_range[1])
        
        bindings = []
        
        # Collect fcurves that drive shapekey values
        for fc in action.fcurves:
            dp = fc.data_path
            if dp.startswith('key_blocks["') and dp.endswith('"].value'):
                # Extract shapekey name
                sk_name = dp[len('key_blocks["'):-len('"].value')]
                
                # Check if this shape key exists on the object
                if sk_name not in obj.data.shape_keys.key_blocks:
                    continue
                
                keys = []
                for kp in fc.keyframe_points:
                    frame = kp.co[0]
                    value = kp.co[1]
                    
                    # Filter by frame range if specified
                    if props.use_frame_range and (frame < frame_start or frame > frame_end):
                        continue
                    
                    t = frame / fps  # Convert to seconds for Unity
                    
                    # Extract interpolation data
                    interpolation = kp.interpolation
                    in_tangent = [float(kp.handle_left[0] - kp.co[0]) / fps, float(kp.handle_left[1] - kp.co[1])]
                    out_tangent = [float(kp.handle_right[0] - kp.co[0]) / fps, float(kp.handle_right[1] - kp.co[1])]
                    
                    keyframe_data = {
                        "time": round(float(t), 6),
                        "value": float(value),
                        "interpolation": interpolation,
                        "inTangent": in_tangent,
                        "outTangent": out_tangent
                    }
                    keys.append(keyframe_data)
                
                if keys:  # Only add if there are keyframes
                    binding = {
                        "path": obj.name,
                        "property": f"blendShape.{sk_name}",
                        "keys": keys
                    }
                    bindings.append(binding)
        
        # If export_all_keys is enabled, add shape keys without animation
        if props.export_all_keys:
            animated_keys = set()
            for binding in bindings:
                prop = binding["property"]
                if prop.startswith("blendShape."):
                    animated_keys.add(prop[11:])  # Remove "blendShape." prefix
            
            for key_block in obj.data.shape_keys.key_blocks:
                if key_block.name != "Basis" and key_block.name not in animated_keys:
                    # Add keyframes with the current value (linear interpolation)
                    t_start = frame_start / fps
                    t_end = frame_end / fps
                    keys = [
                        {
                            "time": round(float(t_start), 6),
                            "value": float(key_block.value),
                            "interpolation": "LINEAR",
                            "inTangent": [0.0, 0.0],
                            "outTangent": [0.0, 0.0]
                        },
                        {
                            "time": round(float(t_end), 6),
                            "value": float(key_block.value),
                            "interpolation": "LINEAR",
                            "inTangent": [0.0, 0.0],
                            "outTangent": [0.0, 0.0]
                        }
                    ]
                    binding = {
                        "path": obj.name,
                        "property": f"blendShape.{key_block.name}",
                        "keys": keys
                    }
                    bindings.append(binding)
        
        # Create the clip data
        clip = {
            "clip_name": action.name,
            "fps": fps,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "duration": (frame_end - frame_start + 1) / fps,
            "object_name": obj.name,
            "bindings": bindings
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write JSON file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(clip, f, ensure_ascii=False, indent=2)
    
    def invoke(self, context, event):
        # Set default filename based on action name
        props = context.scene.animation_export_props
        obj = context.active_object
        
        if obj and obj.animation_data and obj.animation_data.action:
            action_name = obj.animation_data.action.name
            self.filepath = f"{action_name}_blendshape.json"
        else:
            self.filepath = "blendshape_animation.json"
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
