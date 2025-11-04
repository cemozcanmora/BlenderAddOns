import bpy

class OBJECT_OT_split_shape_key_lr(bpy.types.Operator):
    bl_idname = "object.split_shape_key_lr"
    bl_label = "Split Shape Key Left/Right"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Enable only if an object with shape keys is selected
        obj = context.object
        props = context.scene.split_shape_key_props
        return (obj and 
                obj.type == 'MESH' and 
                obj.data.shape_keys and 
                props.shape_key_name and 
                props.shape_key_name in obj.data.shape_keys.key_blocks)

    def execute(self, context):
        obj = context.object
        props = context.scene.split_shape_key_props
        base_shape_name = props.shape_key_name
        
        # Check if shape keys with these names already exist
        left_shape = base_shape_name + "_Left"
        right_shape = base_shape_name + "_Right"
        
        shape_keys = obj.data.shape_keys.key_blocks
        
        # Check if the target shape keys already exist
        if left_shape in shape_keys or right_shape in shape_keys:
            self.report({'WARNING'}, f"Shape keys with names '{left_shape}' or '{right_shape}' already exist. They will be overwritten.")
            
            # If they exist, remove them first
            if left_shape in shape_keys:
                obj.shape_key_remove(shape_keys[left_shape])
            if right_shape in shape_keys:
                obj.shape_key_remove(shape_keys[right_shape])

        # Create temporary vertex groups for left (X > 0) and right (X < 0) sides
        left_group = obj.vertex_groups.new(name="__temp_left")
        right_group = obj.vertex_groups.new(name="__temp_right")

        for v in obj.data.vertices:
            if v.co.x > 0:  # Left side (X > 0)
                left_group.add([v.index], 1.0, 'ADD')
            elif v.co.x < 0:  # Right side (X < 0)
                right_group.add([v.index], 1.0, 'ADD')

        # Add new shape keys
        obj.shape_key_add(name=left_shape, from_mix=False)
        obj.shape_key_add(name=right_shape, from_mix=False)

        # Copy shape data from original to left/right shape keys
        def copy_shape_data(target, direction):
            original = obj.data.shape_keys.key_blocks[base_shape_name]
            basis = obj.data.shape_keys.key_blocks["Basis"]
            target_shape = obj.data.shape_keys.key_blocks[target]

            for i, v in enumerate(obj.data.vertices):
                is_left = direction == "LEFT" and v.co.x > 0  # Left side (X > 0)
                is_right = direction == "RIGHT" and v.co.x < 0  # Right side (X < 0)
                if is_left or is_right:
                    target_shape.data[i].co = original.data[i].co
                else:
                    target_shape.data[i].co = basis.data[i].co

        # Apply shape data to the new shape keys
        copy_shape_data(left_shape, "LEFT")
        copy_shape_data(right_shape, "RIGHT")

        # Clean up temporary vertex groups
        obj.vertex_groups.remove(left_group)
        obj.vertex_groups.remove(right_group)

        self.report({'INFO'}, f"Shape key '{base_shape_name}' split into '{left_shape}' and '{right_shape}'")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_split_shape_key_lr)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_split_shape_key_lr)
