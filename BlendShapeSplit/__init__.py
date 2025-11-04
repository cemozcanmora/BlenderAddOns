bl_info = {
    "name": "Split Shape Key Left/Right",
    "author": "ChatGPT x Udo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Sidebar > Shape Key Tools",
    "description": "Split a symmetric shape key into left and right",
    "category": "Object",
}

import bpy
from . import properties
from . import operators
from . import ui

def register():
    properties.register()
    operators.register()
    ui.register()

def unregister():
    ui.unregister()
    operators.unregister()
    properties.unregister()

if __name__ == "__main__":
    register()
