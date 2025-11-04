bl_info = {
    "name": "Vertex Group Assigner",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Vertex Group Assigner",
    "description": "Assigns vertex groups to vertices with specific materials",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, FloatProperty, BoolProperty, PointerProperty

class VGASettings(PropertyGroup):
    vertex_group_name: StringProperty(
        name="Vertex Group",
        description="Name of the vertex group to assign",
        default="SkinVerts"
    )
    
    material_search: StringProperty(
        name="Material Contains",
        description="Assign to vertices with materials containing this text (case insensitive)",
        default="skin"
    )
    
    case_sensitive: BoolProperty(
        name="Case Sensitive",
        description="Make material name search case sensitive",
        default=False
    )

class VGA_OT_AssignVertexGroup(Operator):
    bl_idname = "vga.assign_vertex_group"
    bl_label = "Assign Vertex Group"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.vga_settings
        vertex_group_name = props.vertex_group_name
        material_search = props.material_search
        case_sensitive = props.case_sensitive
        
        if not material_search:
            self.report({'WARNING'}, "Please specify material search text")
            return {'CANCELLED'}
            
        if not vertex_group_name:
            self.report({'WARNING'}, "Please specify a vertex group name")
            return {'CANCELLED'}
        
        processed_objects = 0
        processed_verts = 0
        
        search_term = material_search if case_sensitive else material_search.lower()
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
                
            mesh = obj.data
            
            # Create or get vertex group
            vgroup = obj.vertex_groups.get(vertex_group_name)
            if not vgroup:
                vgroup = obj.vertex_groups.new(name=vertex_group_name)
            else:
                # Clear existing weights
                vgroup.remove(range(len(mesh.vertices)))
            
            # Get material indices that match our search
            material_indices = []
            for i, mat in enumerate(obj.data.materials):
                if not mat:
                    continue
                    
                mat_name = mat.name if case_sensitive else mat.name.lower()
                if search_term in mat_name:
                    material_indices.append(i)
            
            if not material_indices:
                continue
                
            # Get vertex indices that use these materials
            verts_to_assign = set()
            for poly in mesh.polygons:
                if poly.material_index in material_indices:
                    verts_to_assign.update(poly.vertices[:])
            
            # Assign weights
            if verts_to_assign:
                weight = 1.0
                for v_idx in verts_to_assign:
                    vgroup.add([v_idx], weight, 'REPLACE')
                processed_verts += len(verts_to_assign)
                processed_objects += 1
        
        if processed_objects > 0:
            self.report(
                {'INFO'}, 
                f"Assigned vertex group to {processed_verts} vertices across {processed_objects} objects"
            )
            return {'FINISHED'}
        else:
            self.report(
                {'WARNING'}, 
                f"No vertices found with materials containing '{material_search}'"
            )
            return {'CANCELLED'}

class VGA_PT_Panel(Panel):
    bl_label = "Vertex Group Assigner"
    bl_idname = "VGA_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VGA'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.vga_settings
        
        layout.prop(props, "vertex_group_name")
        layout.prop(props, "material_search")
        layout.prop(props, "case_sensitive")
        
        layout.operator(
            VGA_OT_AssignVertexGroup.bl_idname,
            text="Assign Vertex Group",
            icon='GROUP_VERTEX'
        )

def register():
    bpy.utils.register_class(VGA_OT_AssignVertexGroup)
    bpy.utils.register_class(VGA_PT_Panel)
    bpy.utils.register_class(VGASettings)
    bpy.types.Scene.vga_settings = PointerProperty(type=VGASettings)

def unregister():
    del bpy.types.Scene.vga_settings
    bpy.utils.unregister_class(VGASettings)
    bpy.utils.unregister_class(VGA_PT_Panel)
    bpy.utils.unregister_class(VGA_OT_AssignVertexGroup)

if __name__ == "__main__":
    register()
