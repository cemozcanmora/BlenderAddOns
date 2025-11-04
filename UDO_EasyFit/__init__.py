bl_info = {
    "name": "UDO EasyFit",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > UDO EasyFit",
    "description": "Tools for importing, modifying, and exporting character models",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
from . import import_fbx
from . import modifier_tools
from . import shapekey_tools
from . import export_tools
from . import ui_panel

def register():
    import_fbx.register()
    modifier_tools.register()
    shapekey_tools.register()
    export_tools.register()
    ui_panel.register()

def unregister():
    ui_panel.unregister()
    export_tools.unregister()
    shapekey_tools.unregister()
    modifier_tools.unregister()
    import_fbx.unregister()

if __name__ == "__main__":
    register()
