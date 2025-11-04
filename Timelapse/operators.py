import bpy
import os
from . import utils

class TIMELAPSE_OT_event_tracker(bpy.types.Operator):
    """Modal operator that tracks mouse and keyboard events"""
    bl_idname = "timelapse.event_tracker"
    bl_label = "Event Tracker"
    
    def modal(self, context, event):
        props = context.scene.timelapse
        
        # Stop tracking if recording is stopped
        if not props.is_recording:
            return {'FINISHED'}
        
        # Track events based on interval mode
        should_count = False
        
        if props.interval_mode == 'MOUSE':
            # Count mouse button clicks
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE'} and event.value == 'PRESS':
                should_count = True
        
        elif props.interval_mode == 'KEYBOARD':
            # Count keyboard presses (excluding modifier keys)
            if event.type not in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_CTRL', 'RIGHT_CTRL', 
                                  'LEFT_ALT', 'RIGHT_ALT', 'OSKEY', 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE',
                                  'TIMER', 'TIMER_REPORT', 'TIMERREGION', 'WINDOW_DEACTIVATE'} \
               and event.value == 'PRESS':
                should_count = True
        
        elif props.interval_mode == 'INPUT':
            # Count both mouse clicks and keyboard presses
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE'} and event.value == 'PRESS':
                should_count = True
            elif event.type not in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_CTRL', 'RIGHT_CTRL',
                                    'LEFT_ALT', 'RIGHT_ALT', 'OSKEY', 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE',
                                    'TIMER', 'TIMER_REPORT', 'TIMERREGION', 'WINDOW_DEACTIVATE'} \
                 and event.value == 'PRESS':
                should_count = True
        
        # Increment counter and check if it's time to capture
        if should_count:
            props.event_counter += 1
            
            if props.event_counter >= props.capture_interval:
                props.event_counter = 0
                # Capture frame
                self.capture_timelapse_frame(context)
        
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def capture_timelapse_frame(self, context):
        """Capture a timelapse frame"""
        props = context.scene.timelapse
        
        # Check if timelapse scene exists
        if props.scene_name not in bpy.data.scenes:
            return
        
        timelapse_scene = bpy.data.scenes[props.scene_name]
        camera = timelapse_scene.camera
        
        # Update camera framing if enabled
        if props.auto_frame and props.target_object and camera:
            utils.update_camera_framing(
                camera,
                props.target_object,
                props.camera_distance_multiplier
            )
        
        # Render frame
        output_path = bpy.path.abspath(props.output_path)
        try:
            utils.render_timelapse_frame(timelapse_scene, output_path, props.frame_counter)
            props.frame_counter += 1
        except Exception as e:
            print(f"Error capturing timelapse frame: {e}")

class TIMELAPSE_OT_start_recording(bpy.types.Operator):
    """Start timelapse recording"""
    bl_idname = "timelapse.start_recording"
    bl_label = "Start Recording"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        # Check if target object is set
        if props.target_object is None:
            # Use active object if no target set
            if context.active_object:
                props.target_object = context.active_object
            else:
                self.report({'ERROR'}, "No object selected. Please select an object to track.")
                return {'CANCELLED'}
        
        # Check if scene already exists
        if props.scene_name in bpy.data.scenes:
            self.report({'WARNING'}, f"Scene '{props.scene_name}' already exists. Using existing scene.")
            timelapse_scene = bpy.data.scenes[props.scene_name]
            camera = timelapse_scene.camera
        else:
            # Create timelapse scene
            timelapse_scene, camera = utils.create_timelapse_scene(
                props.scene_name,
                props.target_object,
                props.camera_angle,
                props.camera_distance_multiplier
            )
        
        # Create output directory if it doesn't exist
        output_path = bpy.path.abspath(props.output_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Reset counters
        props.frame_counter = 0
        props.update_counter = 0
        props.event_counter = 0
        
        # Start recording
        props.is_recording = True
        
        # Start event tracker for mouse/keyboard modes
        if props.interval_mode in {'MOUSE', 'KEYBOARD', 'INPUT'}:
            bpy.ops.timelapse.event_tracker('INVOKE_DEFAULT')
        
        mode_text = {
            'DEPSGRAPH': 'scene updates',
            'MOUSE': 'mouse clicks',
            'KEYBOARD': 'keyboard strokes',
            'INPUT': 'input events'
        }.get(props.interval_mode, 'events')
        
        self.report({'INFO'}, f"Timelapse recording started ({mode_text}). Scene: '{props.scene_name}'")
        return {'FINISHED'}

class TIMELAPSE_OT_stop_recording(bpy.types.Operator):
    """Stop timelapse recording"""
    bl_idname = "timelapse.stop_recording"
    bl_label = "Stop Recording"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        if not props.is_recording:
            self.report({'WARNING'}, "Timelapse is not currently recording.")
            return {'CANCELLED'}
        
        # Stop recording
        props.is_recording = False
        
        self.report({'INFO'}, f"Timelapse recording stopped. {props.frame_counter} frames captured.")
        return {'FINISHED'}

class TIMELAPSE_OT_capture_frame(bpy.types.Operator):
    """Manually capture a timelapse frame"""
    bl_idname = "timelapse.capture_frame"
    bl_label = "Capture Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        # Check if scene exists
        if props.scene_name not in bpy.data.scenes:
            self.report({'ERROR'}, "Timelapse scene not found. Start recording first.")
            return {'CANCELLED'}
        
        timelapse_scene = bpy.data.scenes[props.scene_name]
        camera = timelapse_scene.camera
        
        # Update camera framing if auto-frame is enabled
        if props.auto_frame and props.target_object and camera:
            utils.update_camera_framing(
                camera,
                props.target_object,
                props.camera_distance_multiplier
            )
        
        # Render frame
        output_path = bpy.path.abspath(props.output_path)
        utils.render_timelapse_frame(timelapse_scene, output_path, props.frame_counter)
        
        props.frame_counter += 1
        
        self.report({'INFO'}, f"Frame {props.frame_counter} captured.")
        return {'FINISHED'}

class TIMELAPSE_OT_view_scene(bpy.types.Operator):
    """Switch to timelapse scene"""
    bl_idname = "timelapse.view_scene"
    bl_label = "View Timelapse Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        if props.scene_name not in bpy.data.scenes:
            self.report({'ERROR'}, "Timelapse scene not found.")
            return {'CANCELLED'}
        
        context.window.scene = bpy.data.scenes[props.scene_name]
        
        self.report({'INFO'}, f"Switched to scene '{props.scene_name}'")
        return {'FINISHED'}

class TIMELAPSE_OT_reset(bpy.types.Operator):
    """Reset timelapse settings and delete scene"""
    bl_idname = "timelapse.reset"
    bl_label = "Reset Timelapse"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        # Stop recording if active
        props.is_recording = False
        
        # Delete timelapse scene if it exists
        if props.scene_name in bpy.data.scenes:
            timelapse_scene = bpy.data.scenes[props.scene_name]
            bpy.data.scenes.remove(timelapse_scene)
        
        # Reset counters
        props.frame_counter = 0
        props.update_counter = 0
        
        self.report({'INFO'}, "Timelapse reset.")
        return {'FINISHED'}

class TIMELAPSE_OT_update_camera(bpy.types.Operator):
    """Update camera position to frame object"""
    bl_idname = "timelapse.update_camera"
    bl_label = "Update Camera"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.timelapse
        
        if props.scene_name not in bpy.data.scenes:
            self.report({'ERROR'}, "Timelapse scene not found.")
            return {'CANCELLED'}
        
        if props.target_object is None:
            self.report({'ERROR'}, "No target object set.")
            return {'CANCELLED'}
        
        timelapse_scene = bpy.data.scenes[props.scene_name]
        camera = timelapse_scene.camera
        
        if camera:
            utils.position_camera_to_object(
                camera,
                props.target_object,
                props.camera_angle,
                props.camera_distance_multiplier
            )
            self.report({'INFO'}, "Camera updated.")
        else:
            self.report({'ERROR'}, "No camera found in timelapse scene.")
            return {'CANCELLED'}
        
        return {'FINISHED'}

# Handler for automatic frame capture
def timelapse_update_handler(scene, depsgraph):
    """Handler called on depsgraph updates"""
    
    # Only process if we're in the main scene
    if not hasattr(scene, 'timelapse'):
        return
    
    props = scene.timelapse
    
    # Only process if recording is active and in DEPSGRAPH mode
    if not props.is_recording or props.interval_mode != 'DEPSGRAPH':
        return
    
    # Increment update counter
    props.update_counter += 1
    
    # Check if it's time to capture a frame
    if props.update_counter >= props.capture_interval:
        props.update_counter = 0
        
        # Check if timelapse scene exists
        if props.scene_name not in bpy.data.scenes:
            return
        
        timelapse_scene = bpy.data.scenes[props.scene_name]
        camera = timelapse_scene.camera
        
        # Update camera framing if enabled
        if props.auto_frame and props.target_object and camera:
            utils.update_camera_framing(
                camera,
                props.target_object,
                props.camera_distance_multiplier
            )
        
        # Render frame
        output_path = bpy.path.abspath(props.output_path)
        try:
            utils.render_timelapse_frame(timelapse_scene, output_path, props.frame_counter)
            props.frame_counter += 1
        except Exception as e:
            print(f"Error capturing timelapse frame: {e}")

classes = (
    TIMELAPSE_OT_event_tracker,
    TIMELAPSE_OT_start_recording,
    TIMELAPSE_OT_stop_recording,
    TIMELAPSE_OT_capture_frame,
    TIMELAPSE_OT_view_scene,
    TIMELAPSE_OT_reset,
    TIMELAPSE_OT_update_camera,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
