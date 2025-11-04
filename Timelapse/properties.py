import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    PointerProperty,
)

class TimelapseProperties(bpy.types.PropertyGroup):
    """Properties for timelapse recording"""
    
    is_recording: BoolProperty(
        name="Is Recording",
        description="Whether timelapse is currently recording",
        default=False
    )
    
    target_object: PointerProperty(
        name="Target Object",
        description="Object to track with the timelapse camera",
        type=bpy.types.Object
    )
    
    interval_mode: EnumProperty(
        name="Interval Mode",
        description="How to measure capture intervals",
        items=[
            ('DEPSGRAPH', "Scene Updates", "Capture based on scene changes (depsgraph updates)"),
            ('MOUSE', "Mouse Clicks", "Capture every N mouse clicks"),
            ('KEYBOARD', "Keyboard Strokes", "Capture every N keyboard presses"),
            ('INPUT', "Any Input", "Capture every N mouse clicks or keyboard presses"),
        ],
        default='MOUSE'
    )
    
    capture_interval: IntProperty(
        name="Capture Interval",
        description="Number of events between captures (clicks, keystrokes, or scene updates)",
        default=5,
        min=1,
        max=1000
    )
    
    event_counter: IntProperty(
        name="Event Counter",
        description="Internal counter for tracking input events",
        default=0
    )
    
    update_counter: IntProperty(
        name="Update Counter",
        description="Internal counter for tracking updates",
        default=0
    )
    
    frame_counter: IntProperty(
        name="Frame Counter",
        description="Number of frames captured",
        default=0
    )
    
    camera_distance_multiplier: FloatProperty(
        name="Camera Distance",
        description="Multiplier for camera distance from object",
        default=2.5,
        min=1.0,
        max=10.0
    )
    
    output_path: StringProperty(
        name="Output Path",
        description="Directory to save timelapse frames",
        default="//timelapse/",
        subtype='DIR_PATH'
    )
    
    scene_name: StringProperty(
        name="Scene Name",
        description="Name of the timelapse scene",
        default="Timelapse_Scene"
    )
    
    camera_angle: EnumProperty(
        name="Camera Angle",
        description="Default camera viewing angle",
        items=[
            ('FRONT', "Front", "Front view"),
            ('BACK', "Back", "Back view"),
            ('LEFT', "Left", "Left view"),
            ('RIGHT', "Right", "Right view"),
            ('TOP', "Top", "Top view"),
            ('PERSPECTIVE', "Perspective", "3/4 perspective view"),
        ],
        default='PERSPECTIVE'
    )
    
    auto_frame: BoolProperty(
        name="Auto Frame",
        description="Automatically adjust camera to frame object",
        default=True
    )
    
    last_mouse_x: IntProperty(
        name="Last Mouse X",
        description="Last recorded mouse X position",
        default=-1
    )
    
    last_mouse_y: IntProperty(
        name="Last Mouse Y",
        description="Last recorded mouse Y position",
        default=-1
    )

def register():
    bpy.utils.register_class(TimelapseProperties)
    bpy.types.Scene.timelapse = PointerProperty(type=TimelapseProperties)

def unregister():
    del bpy.types.Scene.timelapse
    bpy.utils.unregister_class(TimelapseProperties)
