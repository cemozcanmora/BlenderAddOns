bl_info = {
    "name": "Animation Exporter",
    "author": "Animation Tools",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Animation Export",
    "description": "Export blendshape animations as JSON files for Unity",
    "category": "Animation",
}

import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Panel, Operator, PropertyGroup

from . import operators
from . import ui_panel
from . import properties

classes = (
    properties.AnimationExportProperties,
    operators.ANIM_OT_export_blendshape,
    ui_panel.ANIM_PT_export_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.animation_export_props = bpy.props.PointerProperty(
        type=properties.AnimationExportProperties
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.animation_export_props

if __name__ == "__main__":
    register()
