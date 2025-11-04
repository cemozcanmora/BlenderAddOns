bl_info = {
    "name": "Timelapse Recorder",
    "author": "Your Name",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Timelapse",
    "description": "Automatically create timelapses with dynamic camera positioning and event-based capture",
    "category": "Animation",
}

import bpy
from . import properties
from . import operators
from . import panel
from . import utils

modules = [
    properties,
    operators,
    panel,
]

def register():
    for module in modules:
        module.register()
    
    # Register app handlers
    bpy.app.handlers.depsgraph_update_post.append(operators.timelapse_update_handler)

def unregister():
    # Unregister app handlers
    if operators.timelapse_update_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(operators.timelapse_update_handler)
    
    for module in reversed(modules):
        module.unregister()

if __name__ == "__main__":
    register()
