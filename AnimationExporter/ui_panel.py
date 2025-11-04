import bpy
from bpy.types import Panel

class ANIM_PT_export_panel(Panel):
    """Panel for Animation Export settings"""
    bl_label = "Animation Exporter"
    bl_idname = "ANIM_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Animation Export"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.animation_export_props
        obj = context.active_object
        
        # Object info
        box = layout.box()
        box.label(text="Object Info", icon='OBJECT_DATA')
        
        if obj:
            box.label(text=f"Active: {obj.name}")
            if obj.type == 'MESH':
                if obj.data.shape_keys:
                    key_count = len(obj.data.shape_keys.key_blocks) - 1  # Exclude Basis
                    box.label(text=f"Shape Keys: {key_count}", icon='SHAPEKEY_DATA')
                else:
                    box.label(text="No Shape Keys", icon='ERROR')
            else:
                box.label(text="Not a Mesh", icon='ERROR')
        else:
            box.label(text="No Active Object", icon='ERROR')
        
        layout.separator()
        
        # Action Selection
        box = layout.box()
        box.label(text="Action Selection", icon='ACTION')
        
        col = box.column()
        col.prop(props, "use_active_action")
        
        if not props.use_active_action:
            col.prop(props, "selected_action")
        
        # Show current action info
        if obj and obj.animation_data:
            if obj.animation_data.action:
                action = obj.animation_data.action
                col.label(text=f"Current: {action.name}")
                frame_range = f"{int(action.frame_range[0])}-{int(action.frame_range[1])}"
                col.label(text=f"Frames: {frame_range}")
            else:
                col.label(text="No Active Action", icon='ERROR')
        
        layout.separator()
        
        # Export Options
        box = layout.box()
        box.label(text="Export Options", icon='EXPORT')
        
        col = box.column()
        col.prop(props, "export_all_keys")
        col.prop(props, "use_frame_range")
        
        if props.use_frame_range:
            row = col.row(align=True)
            row.prop(props, "frame_start")
            row.prop(props, "frame_end")
        
        layout.separator()
        
        # Export Button
        row = layout.row()
        row.scale_y = 2.0
        
        # Check if export is possible
        can_export = True
        error_msg = ""
        
        if not obj:
            can_export = False
            error_msg = "No active object"
        elif obj.type != 'MESH':
            can_export = False
            error_msg = "Object is not a mesh"
        elif not obj.data.shape_keys:
            can_export = False
            error_msg = "No shape keys"
        elif props.use_active_action:
            if not (obj.animation_data and obj.animation_data.action):
                can_export = False
                error_msg = "No active action"
        else:
            if props.selected_action == "NONE":
                can_export = False
                error_msg = "No action selected"
        
        if can_export:
            row.operator("anim.export_blendshape", icon='EXPORT')
        else:
            row.enabled = False
            row.operator("anim.export_blendshape", icon='ERROR', text=f"Export ({error_msg})")
        
        # Info section
        if obj and obj.data.shape_keys and obj.animation_data and obj.animation_data.action:
            layout.separator()
            box = layout.box()
            box.label(text="Animation Info", icon='INFO')
            
            action = obj.animation_data.action
            shape_key_fcurves = 0
            
            for fc in action.fcurves:
                if fc.data_path.startswith('key_blocks["') and fc.data_path.endswith('"].value'):
                    shape_key_fcurves += 1
            
            box.label(text=f"Animated Shape Keys: {shape_key_fcurves}")
            box.label(text=f"Total Keyframes: {sum(len(fc.keyframe_points) for fc in action.fcurves)}")
            
            fps = context.scene.render.fps
            duration = (action.frame_range[1] - action.frame_range[0] + 1) / fps
            box.label(text=f"Duration: {duration:.2f}s @ {fps} fps")
