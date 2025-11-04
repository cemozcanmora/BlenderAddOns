import bpy
from bpy.types import Panel, PropertyGroup
from bpy.props import PointerProperty, StringProperty

# Define property group to store mesh references
class UDO_EasyFit_Properties(PropertyGroup):
    target_mesh: PointerProperty(
        name="Target Mesh",
        description="Select the target mesh",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    source_mesh: PointerProperty(
        name="Source Mesh",
        description="Select the source mesh",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH'
    )

# Define the main panel
class UDO_PT_EasyFit_Panel(Panel):
    bl_label = "UDO Easy Fit"
    bl_idname = "UDO_PT_EasyFit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UDO EasyFit"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.udo_easyfit_props
        
        # Target mesh selection
        box = layout.box()
        box.label(text="Target mesh")
        box.prop(props, "target_mesh", text="")
        
        # Source mesh selection
        box = layout.box()
        box.label(text="Source mesh")
        box.prop(props, "source_mesh", text="")
        
        # Actions section
        box = layout.box()
        box.label(text="Actions")
        box.operator("udo.apply_easyfit_to_source", text="Apply")

# Registration
def register():
    bpy.utils.register_class(UDO_EasyFit_Properties)
    bpy.utils.register_class(UDO_PT_EasyFit_Panel)
    bpy.types.Scene.udo_easyfit_props = PointerProperty(type=UDO_EasyFit_Properties)

def unregister():
    del bpy.types.Scene.udo_easyfit_props
    bpy.utils.unregister_class(UDO_PT_EasyFit_Panel)
    bpy.utils.unregister_class(UDO_EasyFit_Properties)

if __name__ == "__main__":
    register()
