bl_info = {
    "name": "UDOport",
    "author": "UDO Tools",
    "version": (2, 0, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > UDOport",
    "description": "Export FBX files and blendshape animations to Unity with mesh, armature, and empty objects",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Panel, Operator, PropertyGroup

from . import export_fbx
from . import animation_export
from . import ui_panel
from . import name_utils
from . import properties

classes = (
    properties.AnimationExportProperties,
    export_fbx.UDO_OT_ExportFBXToUnity,
    animation_export.UDO_OT_export_blendshape,
    name_utils.UDO_OT_RemoveNumericSuffixes,
    ui_panel.UDO_PT_ExporterPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register animation export properties
    bpy.types.Scene.animation_export_props = bpy.props.PointerProperty(
        type=properties.AnimationExportProperties
    )
    
    # Register FBX export properties
    bpy.types.Scene.udo_export_animation = bpy.props.BoolProperty(
        name="Export Animation",
        description="Export animation data with the FBX file",
        default=True
    )
    
    bpy.types.Scene.udo_apply_transforms = bpy.props.BoolProperty(
        name="Apply Transforms",
        description="Apply location, rotation, and scale transforms to all selected objects before export",
        default=True
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove properties
    del bpy.types.Scene.animation_export_props
    del bpy.types.Scene.udo_export_animation
    del bpy.types.Scene.udo_apply_transforms

if __name__ == "__main__":
    register()
