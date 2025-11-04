import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty

def get_addon_path():
    """Get the path to the addon directory"""
    return os.path.dirname(os.path.realpath(__file__))

def append_easyfit_node_tree(context):
    """Append the easyfit node tree from the ClothAutomation.blend file"""
    addon_path = get_addon_path()
    blend_file_path = os.path.join(addon_path, "ClothAutomation.blend")
    
    # Check if the file exists
    if not os.path.exists(blend_file_path):
        return False, "ClothAutomation.blend file not found in addon directory"
    
    # Check if the node tree is already in the blend file
    easyfit_exists = False
    easyfit_node_tree = None
    for node_group in bpy.data.node_groups:
        if node_group.name == "easyfit" or node_group.name.startswith("easyfit."):
            easyfit_exists = True
            easyfit_node_tree = node_group
            break
    
    # If not already imported, append the node tree
    if not easyfit_exists:
        # Specify the directory inside the .blend file and the object to append
        inner_path = 'NodeTree'
        node_name = 'easyfit'
        
        try:
            # Use the low-level append function
            bpy.ops.wm.append(
                filepath=os.path.join(blend_file_path, inner_path, node_name),
                directory=os.path.join(blend_file_path, inner_path),
                filename=node_name
            )
            
            # Check if append was successful
            success = False
            for node_group in bpy.data.node_groups:
                if node_group.name == "easyfit" or node_group.name.startswith("easyfit."):
                    easyfit_node_tree = node_group
                    success = True
                    break
                    
            if success:
                return True, easyfit_node_tree
            else:
                return False, "Failed to append 'easyfit' node tree, node tree not found after append operation"
        
        except Exception as e:
            return False, f"Error appending 'easyfit' node tree: {str(e)}"
    else:
        return True, easyfit_node_tree

def apply_geometry_nodes_modifier(obj, node_tree, target_mesh=None):
    """Apply a Geometry Nodes modifier with the given node tree to an object"""
    if obj is None:
        return False, "No object selected"
    
    if obj.type != 'MESH':
        return False, "Selected object is not a mesh"
    
    # Check if the object already has a geometry nodes modifier with this node tree
    for modifier in obj.modifiers:
        if modifier.type == 'NODES' and modifier.node_group == node_tree:
            # Already has the modifier with this node tree, update target mesh if provided
            if target_mesh is not None:
                try:
                    # Set input 2 (Target Mesh) to the target mesh
                    modifier["Input_2"] = target_mesh
                except Exception as e:
                    return False, f"Error setting target mesh: {str(e)}"
            return True, f"Object '{obj.name}' already has the EasyFit geometry nodes modifier"
    
    # Add a new Geometry Nodes modifier
    try:
        gn_modifier = obj.modifiers.new(name="EasyFit", type='NODES')
        gn_modifier.node_group = node_tree
        
        # Set input 2 (Target Mesh) to the target mesh if provided
        if target_mesh is not None:
            try:
                gn_modifier["Input_2"] = target_mesh
            except Exception as e:
                return False, f"Error setting target mesh: {str(e)}"
        
        return True, f"Successfully applied EasyFit geometry nodes modifier to '{obj.name}'"
    except Exception as e:
        return False, f"Error applying geometry nodes modifier: {str(e)}"

class UDO_OT_ApplyEasyFitToSourceMesh(Operator):
    """Apply the EasyFit geometry nodes to the source mesh"""
    bl_idname = "udo.apply_easyfit_to_source"
    bl_label = "Apply EasyFit to Source"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if we're in object mode and a source mesh is selected
        props = context.scene.udo_easyfit_props
        return context.mode == 'OBJECT' and props.source_mesh is not None
    
    def execute(self, context):
        props = context.scene.udo_easyfit_props
        source_mesh = props.source_mesh
        target_mesh = props.target_mesh
        
        # Make sure we have a source mesh
        if source_mesh is None:
            self.report({'ERROR'}, "Please select a source mesh first")
            return {'CANCELLED'}
        
        # First ensure we have the easyfit node tree
        success, result = append_easyfit_node_tree(context)
        
        if not success:
            self.report({'ERROR'}, str(result))
            return {'CANCELLED'}
        
        # Now we have the node tree, apply it as a modifier
        node_tree = result  # The result contains the node tree if successful
        success, message = apply_geometry_nodes_modifier(source_mesh, node_tree, target_mesh)
        
        if success:
            self.report({'INFO'}, message)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(UDO_OT_ApplyEasyFitToSourceMesh)

def unregister():
    bpy.utils.unregister_class(UDO_OT_ApplyEasyFitToSourceMesh)

if __name__ == "__main__":
    register()
