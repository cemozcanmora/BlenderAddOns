import bpy

class OBJECT_PT_shape_key_splitter(bpy.types.Panel):
    bl_label = "Split Shape Key L/R"
    bl_idname = "OBJECT_PT_shape_key_splitter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shape Key'
    
    @classmethod
    def poll(cls, context):
        # Only show panel for mesh objects
        return context.object and context.object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        props = context.scene.split_shape_key_props
        
        # Message if no shape keys exist
        if not obj.data.shape_keys:
            layout.label(text="No shape keys found")
            layout.label(text="Add shape keys first")
            return
            
        # Display shape key selection
        box = layout.box()
        box.label(text="Select Shape Key to Split:")
        box.prop(props, "shape_key_name", text="")
        
        # Only enable the button if a shape key is selected
        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.split_shape_key_lr", icon="MOD_MIRROR")
        row.enabled = props.shape_key_name != ""

def register():
    bpy.utils.register_class(OBJECT_PT_shape_key_splitter)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_shape_key_splitter)
