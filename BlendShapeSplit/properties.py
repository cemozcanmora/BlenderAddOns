import bpy

def get_shape_keys(self, context):
    items = []
    obj = context.object
    
    if obj and obj.type == 'MESH' and obj.data.shape_keys:
        for key in obj.data.shape_keys.key_blocks:
            # Skip the basis shape key
            if key.name != "Basis":
                items.append((key.name, key.name, f"Select {key.name} shape key"))
    
    # Add a message if no shape keys are found
    if not items:
        items.append(("", "No shape keys found", ""))
        
    return items

class SplitShapeKeyProperties(bpy.types.PropertyGroup):
    shape_key_name: bpy.props.EnumProperty(
        name="Shape Key",
        description="Select the symmetric shape key to split",
        items=get_shape_keys
    )

def register():
    bpy.utils.register_class(SplitShapeKeyProperties)
    bpy.types.Scene.split_shape_key_props = bpy.props.PointerProperty(type=SplitShapeKeyProperties)

def unregister():
    del bpy.types.Scene.split_shape_key_props
    bpy.utils.unregister_class(SplitShapeKeyProperties)
