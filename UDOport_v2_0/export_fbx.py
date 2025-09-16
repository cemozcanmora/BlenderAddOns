import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper
from .name_utils import clean_vertex_group_names

class UDO_OT_ExportFBXToUnity(bpy.types.Operator, ExportHelper):
    """Export selected objects to FBX format optimized for Unity"""
    bl_idname = "udo.export_fbx_to_unity"
    bl_label = "Export FBX to Unity"
    bl_description = "Export selected objects to FBX format optimized for Unity"
    bl_options = {'REGISTER', 'UNDO'}

    # ExportHelper mixin class properties
    filename_ext = ".fbx"
    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
    )

    def clean_vertex_group_names(self, objects):
        """Wrapper for the clean_vertex_group_names function from name_utils"""
        return clean_vertex_group_names(objects, self.report)

    def execute(self, context):
        # Check if any objects are selected
        if not context.selected_objects:
            self.report({'ERROR'}, "No objects selected for export")
            return {'CANCELLED'}
            
        # Clean vertex group names by removing '_Parent' suffix
        self.clean_vertex_group_names(context.selected_objects)
        
        # Filter selected objects to only include mesh, armature, and empty objects
        valid_objects = [obj for obj in context.selected_objects 
                         if obj.type in ('MESH', 'ARMATURE', 'EMPTY')]
        
        if not valid_objects:
            self.report({'ERROR'}, "No valid objects (mesh, armature, or empty) selected for export")
            return {'CANCELLED'}
        
        # Remember original selection
        original_selection = context.selected_objects.copy()
        active_object = context.active_object
        
        # Select only valid objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in valid_objects:
            obj.select_set(True)
        
        # Set an active object if needed
        if not context.active_object or context.active_object not in valid_objects:
            context.view_layer.objects.active = valid_objects[0]
            
        # Apply all transforms to selected objects (if enabled)
        if context.scene.udo_apply_transforms:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # --- Custom Armature Rotation Logic ---
        armatures = [obj for obj in valid_objects if obj.type == 'ARMATURE']
        rotated_armatures = []
        try:
            for arm in armatures:
                # Rotate X by -90
                arm.rotation_euler.rotate_axis('X', -1.5708)  # -90 deg in radians
                bpy.context.view_layer.update()
                # Apply rotation
                bpy.ops.object.select_all(action='DESELECT')
                arm.select_set(True)
                context.view_layer.objects.active = arm
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                # Rotate X by +90
                arm.rotation_euler.rotate_axis('X', 1.5708)  # +90 deg in radians
                bpy.context.view_layer.update()
                rotated_armatures.append(arm)

            # Reselect valid objects for export
            bpy.ops.object.select_all(action='DESELECT')
            for obj in valid_objects:
                obj.select_set(True)
            context.view_layer.objects.active = valid_objects[0]

            # Export FBX with default settings
            result = bpy.ops.export_scene.fbx(
                filepath=self.filepath,
                check_existing=True,
                use_selection=True,
                use_active_collection=False,
                global_scale=1.0,
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL',
                axis_forward='-Z',
                axis_up='Y',
                object_types={'MESH', 'ARMATURE', 'EMPTY'},
                bake_space_transform=True,
                use_mesh_modifiers=False,
                mesh_smooth_type='OFF',
                use_subsurf=False,
                use_mesh_edges=False,
                use_tspace=False,
                use_custom_props=True,
                add_leaf_bones=False,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=False,
                armature_nodetype='NULL',
                bake_anim=context.scene.udo_export_animation,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=True,
                bake_anim_use_all_actions=True,
                bake_anim_force_startend_keying=True,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=1.0,
                path_mode='AUTO',
                embed_textures=False,
                batch_mode='OFF',
                use_batch_own_dir=True,
            )
        finally:
            # After export, apply rotation to armature(s) again
            for arm in rotated_armatures:
                bpy.ops.object.select_all(action='DESELECT')
                arm.select_set(True)
                context.view_layer.objects.active = arm
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

            # Restore original selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selection:
                obj.select_set(True)
            context.view_layer.objects.active = active_object

        if result == {'FINISHED'}:
            self.report({'INFO'}, f"FBX exported successfully to {self.filepath}")
        return result
