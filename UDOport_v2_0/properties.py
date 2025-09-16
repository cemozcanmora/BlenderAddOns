import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import PropertyGroup

def get_actions(self, context):
    """Get available actions for the active object"""
    items = [("NONE", "No Action", "No action selected")]
    
    obj = context.active_object
    if obj and obj.animation_data:
        # Add current action if exists
        if obj.animation_data.action:
            current_action = obj.animation_data.action
            items.append((current_action.name, current_action.name, f"Current action: {current_action.name}"))
        
        # Add all actions from the blend file
        for action in bpy.data.actions:
            if action.name not in [item[0] for item in items]:
                items.append((action.name, action.name, f"Action: {action.name}"))
    
    return items

class AnimationExportProperties(PropertyGroup):
    """Properties for animation export settings"""
    
    export_filepath: StringProperty(
        name="Export Path",
        description="Path to export the JSON file",
        default="//blendshape_animation.json",
        subtype='FILE_PATH'
    )
    
    selected_action: EnumProperty(
        name="Action",
        description="Select which action to export",
        items=get_actions,
        default=0
    )
    
    use_active_action: BoolProperty(
        name="Use Active Action",
        description="Export the currently active action on the object",
        default=True
    )
    
    export_all_keys: BoolProperty(
        name="Export All Shape Keys",
        description="Export all shape keys, even if they don't have keyframes",
        default=False
    )
    
    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame for export",
        default=1,
        min=1
    )
    
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for export",
        default=250,
        min=1
    )
    
    use_frame_range: BoolProperty(
        name="Use Frame Range",
        description="Use custom frame range instead of action range",
        default=False
    )
