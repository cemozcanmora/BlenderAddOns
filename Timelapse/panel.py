import bpy

class TIMELAPSE_PT_main_panel(bpy.types.Panel):
    """Main panel for timelapse recording"""
    bl_label = "Timelapse Recorder"
    bl_idname = "TIMELAPSE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Timelapse'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.timelapse
        
        # Status indicator
        box = layout.box()
        row = box.row()
        if props.is_recording:
            row.label(text="● RECORDING", icon='REC')
            row = box.row()
            row.label(text=f"Frames: {props.frame_counter}")
            
            # Show event counter for input-based modes
            if props.interval_mode in {'MOUSE', 'KEYBOARD', 'INPUT'}:
                row = box.row()
                row.label(text=f"Events: {props.event_counter}/{props.capture_interval}")
        else:
            row.label(text="○ Stopped", icon='PAUSE')
        
        layout.separator()
        
        # Target object selection
        box = layout.box()
        box.label(text="Target Object:", icon='OBJECT_DATA')
        box.prop(props, "target_object", text="")
        
        if context.active_object and props.target_object != context.active_object:
            row = box.row()
            row.operator("timelapse.set_active_object", text="Use Active Object", icon='EYEDROPPER')
        
        layout.separator()
        
        # Camera settings
        box = layout.box()
        box.label(text="Camera Settings:", icon='CAMERA_DATA')
        box.prop(props, "camera_angle")
        box.prop(props, "camera_distance_multiplier")
        box.prop(props, "auto_frame")
        
        if props.scene_name in bpy.data.scenes:
            box.operator("timelapse.update_camera", icon='FILE_REFRESH')
        
        layout.separator()
        
        # Recording settings
        box = layout.box()
        box.label(text="Recording Settings:", icon='SETTINGS')
        box.prop(props, "interval_mode")
        
        # Show appropriate label based on mode
        if props.interval_mode == 'DEPSGRAPH':
            box.label(text="Updates per capture:", icon='BLANK1')
        elif props.interval_mode == 'MOUSE':
            box.label(text="Clicks per capture:", icon='BLANK1')
        elif props.interval_mode == 'KEYBOARD':
            box.label(text="Keystrokes per capture:", icon='BLANK1')
        else:  # INPUT
            box.label(text="Inputs per capture:", icon='BLANK1')
        
        box.prop(props, "capture_interval", text="")
        box.prop(props, "output_path")
        box.prop(props, "scene_name")
        
        layout.separator()
        
        # Control buttons
        box = layout.box()
        box.label(text="Controls:", icon='PLAY')
        
        if not props.is_recording:
            box.operator("timelapse.start_recording", text="Start Recording", icon='REC')
        else:
            box.operator("timelapse.stop_recording", text="Stop Recording", icon='SNAP_FACE')
        
        box.operator("timelapse.capture_frame", text="Capture Frame Now", icon='RENDER_STILL')
        
        layout.separator()
        
        # Utility buttons
        box = layout.box()
        box.label(text="Utilities:", icon='TOOL_SETTINGS')
        
        if props.scene_name in bpy.data.scenes:
            box.operator("timelapse.view_scene", icon='SCENE_DATA')
        
        box.operator("timelapse.reset", text="Reset Timelapse", icon='TRASH')

class TIMELAPSE_OT_set_active_object(bpy.types.Operator):
    """Set active object as target"""
    bl_idname = "timelapse.set_active_object"
    bl_label = "Set Active Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.active_object:
            context.scene.timelapse.target_object = context.active_object
            self.report({'INFO'}, f"Target set to '{context.active_object.name}'")
        else:
            self.report({'WARNING'}, "No active object")
        return {'FINISHED'}

classes = (
    TIMELAPSE_PT_main_panel,
    TIMELAPSE_OT_set_active_object,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
