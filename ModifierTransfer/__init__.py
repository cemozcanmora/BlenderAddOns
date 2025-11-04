bl_info = {
    "name": "Modifier Transfer",
    "author": "Cascade",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Modifier Transfer",
    "description": "Copy a chosen modifier from the active object to all selected objects; batch-apply by index.",
    "category": "Object",
}

import importlib
import bpy

# Local imports
from . import utils
from .ops import apply_selected_modifier, apply_index_modifier
from .ui import panel

# Hot-reload during development
if "_reloaded" in locals():
    importlib.reload(utils)
    importlib.reload(apply_selected_modifier)
    importlib.reload(apply_index_modifier)
    importlib.reload(panel)
_reloaded = True

# Properties

def mt_modifier_items(self, context):
    obj = context.active_object
    items = []
    if obj and obj.modifiers:
        for i, m in enumerate(obj.modifiers):
            # identifier, name, description, icon, number
            display = f"{i+1:02d}. {m.name} ({m.type})"
            items.append((m.name, display, f"Modifier {m.type}", i))
    else:
        items.append(("", "No modifiers on active", "", 0))
    return items

class MT_Props(bpy.types.PropertyGroup):
    apply_immediately: bpy.props.BoolProperty(
        name="Apply Immediately",
        description="After adding the copied modifier to each object, apply it immediately",
        default=False,
    )
    modifier_index: bpy.props.IntProperty(
        name="Modifier Index",
        description="1-based index in the modifier stack to apply on each selected object",
        default=1,
        min=1,
    )
    selected_modifier: bpy.props.EnumProperty(
        name="Active's Modifier",
        description="Choose a modifier from the active object to copy to all selected",
        items=mt_modifier_items,
    )


classes = (
    MT_Props,
    apply_selected_modifier.OBJECT_OT_mt_apply_selected_modifier,
    apply_index_modifier.OBJECT_OT_mt_apply_modifier_by_index,
    panel.VIEW3D_PT_mt_modifier_transfer,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mt_props = bpy.props.PointerProperty(type=MT_Props)


def unregister():
    del bpy.types.Scene.mt_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
