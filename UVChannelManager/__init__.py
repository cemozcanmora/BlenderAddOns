bl_info = {
    "name": "UV Channel Manager",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > UV Channel Manager",
    "description": "Manage UV channels across multiple objects",
    "warning": "",
    "doc_url": "",
    "category": "UV",
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, IntProperty, CollectionProperty, BoolProperty
from bpy.utils import register_class, unregister_class

# Property group to store UV channel names
class UVChannelItem(PropertyGroup):
    name: StringProperty(name="UV Channel Name", default="")
    index: IntProperty()

# Operator to add a new UV channel
class UVCHANNEL_OT_AddChannel(Operator):
    bl_idname = "uv_channel.add_channel"
    bl_label = "Add UV Channel"
    bl_options = {'REGISTER', 'UNDO'}
    
    channel_name: StringProperty(name="Channel Name", default="UVChannel")
    
    def execute(self, context):
        scene = context.scene
        uv_channels = scene.uv_channel_items
        
        # Find the next available index
        used_indices = [item.index for item in uv_channels]
        new_index = 0
        while new_index in used_indices:
            new_index += 1
            
        # Add new channel
        new_channel = uv_channels.add()
        new_channel.name = f"{self.channel_name}_{new_index}" if self.channel_name else f"UV_{new_index}"
        new_channel.index = new_index
        
        # Add UV map to selected objects
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if obj.data.uv_layers.active is None or len(obj.data.uv_layers) == 0:
                    # If no UV maps, create a default one
                    obj.data.uv_layers.new(name=new_channel.name)
                else:
                    # Create a new UV map and make it active
                    uv_layer = obj.data.uv_layers.new(name=new_channel.name)
                    obj.data.uv_layers.active = uv_layer
        
        return {'FINISHED'}

# Operator to remove a UV channel by index
class UVCHANNEL_OT_RemoveChannel(Operator):
    bl_idname = "uv_channel.remove_channel"
    bl_label = "Remove UV Channel"
    bl_options = {'REGISTER', 'UNDO'}
    
    channel_index: IntProperty()
    
    def execute(self, context):
        scene = context.scene
        uv_channels = scene.uv_channel_items
        
        # Find and remove the channel from the collection
        for i, channel in enumerate(uv_channels):
            if channel.index == self.channel_index:
                # Remove UV map from selected objects
                for obj in context.selected_objects:
                    if obj.type == 'MESH':
                        uv_layers = obj.data.uv_layers
                        for uv_layer in uv_layers:
                            if uv_layer.name == channel.name:
                                uv_layers.remove(uv_layer)
                                break
                
                # Remove from collection
                uv_channels.remove(i)
                break
        
        return {'FINISHED'}

# Operator to rename a UV channel
class UVCHANNEL_OT_RemoveSecondaryChannels(Operator):
    bl_idname = "uv_channel.remove_secondary_channels"
    bl_label = "Remove All Secondary UV Channels"
    bl_description = "Remove all UV channels except the first one from selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get selected objects that are meshes
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}
            
        removed_count = 0
        
        for obj in selected_objects:
            uv_layers = obj.data.uv_layers
            # Skip if there are 1 or fewer UV maps
            if len(uv_layers) <= 1:
                continue
                
            # Keep track of the first UV map's name
            first_uv_name = uv_layers[0].name
            
            # Remove all UV layers except the first one
            while len(uv_layers) > 1:
                uv_layers.remove(uv_layers[1])
                removed_count += 1
                
            # Ensure the first UV layer is named correctly in our tracking
            if uv_layers and uv_layers[0].name != first_uv_name:
                uv_layers[0].name = first_uv_name
        
        # Update the scene's UV channel items
        scene = context.scene
        uv_channels = scene.uv_channel_items
        
        # Keep only the first UV channel in our tracking
        if len(uv_channels) > 1:
            first_channel_name = uv_channels[0].name
            first_channel_index = uv_channels[0].index
            
            # Clear all and re-add the first one
            uv_channels.clear()
            if removed_count > 0:  # Only add if we actually had UVs to remove
                channel = uv_channels.add()
                channel.name = first_channel_name
                channel.index = first_channel_index
        
        self.report({'INFO'}, f"Removed {removed_count} secondary UV channels")
        return {'FINISHED'}

class UVCHANNEL_OT_RenameChannel(Operator):
    bl_idname = "uv_channel.rename_channel"
    bl_label = "Rename UV Channel"
    bl_options = {'REGISTER', 'UNDO'}
    
    channel_index: IntProperty()
    new_name: StringProperty(name="New Name")
    
    def execute(self, context):
        scene = context.scene
        uv_channels = scene.uv_channel_items
        
        for channel in uv_channels:
            if channel.index == self.channel_index:
                old_name = channel.name
                channel.name = self.new_name
                
                # Update UV map names in selected objects
                for obj in context.selected_objects:
                    if obj.type == 'MESH':
                        for uv_layer in obj.data.uv_layers:
                            if uv_layer.name == old_name:
                                uv_layer.name = self.new_name
                break
        
        return {'FINISHED'}

# Panel in the 3D View sidebar
class VIEW3D_PT_UVChannelManager(Panel):
    bl_label = "UV Channel Manager"
    bl_idname = "VIEW3D_PT_uv_channel_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UV Channel Manager'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Add UV Channel
        box = layout.box()
        box.label(text="Add UV Channel")
        row = box.row()
        row.prop(scene, "new_channel_name", text="")
        op = row.operator("uv_channel.add_channel", text="Add")
        op.channel_name = scene.new_channel_name
        
        # Remove All Secondary UVs
        layout.separator()
        layout.operator("uv_channel.remove_secondary_channels", 
                      text="Remove All Secondary UVs", 
                      icon='X')
        
        # List of UV Channels
        layout.separator()
        layout.label(text="UV Channels:")
        
        for channel in scene.uv_channel_items:
            row = layout.row()
            row.label(text=channel.name)
            
            # Rename button
            op = row.operator("uv_channel.rename_channel", text="", icon='GREASEPENCIL')
            op.channel_index = channel.index
            op.new_name = channel.name
            
            # Remove button
            op = row.operator("uv_channel.remove_channel", text="", icon='X')
            op.channel_index = channel.index

# Properties
classes = (
    UVChannelItem,
    UVCHANNEL_OT_AddChannel,
    UVCHANNEL_OT_RemoveChannel,
    UVCHANNEL_OT_RemoveSecondaryChannels,
    UVCHANNEL_OT_RenameChannel,
    VIEW3D_PT_UVChannelManager,
)

def register():
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.uv_channel_items = CollectionProperty(type=UVChannelItem)
    bpy.types.Scene.new_channel_name = StringProperty(
        name="Channel Name",
        description="Name for the new UV channel",
        default="UVChannel"
    )

def unregister():
    del bpy.types.Scene.uv_channel_items
    del bpy.types.Scene.new_channel_name
    
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
