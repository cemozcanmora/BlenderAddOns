import bpy
from bpy.types import Panel

class UDO_PT_ExporterPanel(Panel):
    """Unity Export Panel"""
    bl_label = "UDOport"
    bl_idname = "UDO_PT_exporter_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UDOport'
    
    def draw(self, context):
        layout = self.layout
        
        # Selection status
        selected_objects = bpy.context.selected_objects
        box = layout.box()
        if selected_objects:
            box.label(text=f"Selected: {len(selected_objects)} objects")
            
            # Count object types
            mesh_count = len([obj for obj in selected_objects if obj.type == 'MESH'])
            armature_count = len([obj for obj in selected_objects if obj.type == 'ARMATURE'])
            empty_count = len([obj for obj in selected_objects if obj.type == 'EMPTY'])
            
            if mesh_count:
                box.label(text=f"Meshes: {mesh_count}")
            if armature_count:
                box.label(text=f"Armatures: {armature_count}")
            if empty_count:
                box.label(text=f"Empties: {empty_count}")
        else:
            box.label(text="No objects selected")
            box.label(text="Select objects to export", icon='ERROR')

        # FBX Export Section
        layout.separator()
        fbx_box = layout.box()
        fbx_box.label(text="FBX Export", icon='EXPORT')
        
        # Export button
        row = fbx_box.row(align=True)
        row.scale_y = 1.5
        export_op = row.operator("udo.export_fbx_to_unity", text="Export FBX to Unity", icon='EXPORT')
        
        # FBX Export options
        options_box = fbx_box.box()
        options_box.label(text="FBX Options:")
        
        # Animation settings
        options_box.prop(context.scene, "udo_export_animation", text="Export Animation")
        
        # Transform settings
        options_box.prop(context.scene, "udo_apply_transforms", text="Apply Transforms")
        
        # Naming tools section
        naming_box = fbx_box.box()
        naming_box.label(text="Naming Tools:", icon='SORTALPHA')
        row = naming_box.row(align=True)
        row.operator("object.remove_numeric_suffixes", 
                    text="Delete Suffixes", 
                    icon='SORTBYEXT')

        # Animation Export Section
        layout.separator()
        anim_box = layout.box()
        anim_box.label(text="Animation Export", icon='ANIM')
        
        props = context.scene.animation_export_props
        obj = context.active_object
        
        # Object info for animation export
        info_box = anim_box.box()
        info_box.label(text="Object Info", icon='OBJECT_DATA')
        
        if obj:
            info_box.label(text=f"Active: {obj.name}")
            if obj.type == 'MESH':
                if obj.data.shape_keys:
                    key_count = len(obj.data.shape_keys.key_blocks) - 1  # Exclude Basis
                    info_box.label(text=f"Shape Keys: {key_count}", icon='SHAPEKEY_DATA')
                else:
                    info_box.label(text="No Shape Keys", icon='ERROR')
            else:
                info_box.label(text="Not a Mesh", icon='ERROR')
        else:
            info_box.label(text="No Active Object", icon='ERROR')
        
        # Action Selection
        action_box = anim_box.box()
        action_box.label(text="Action Selection", icon='ACTION')
        
        col = action_box.column()
        col.prop(props, "use_active_action")
        
        if not props.use_active_action:
            col.prop(props, "selected_action")
        
        # Show current action info
        if obj and obj.animation_data:
            if obj.animation_data.action:
                action = obj.animation_data.action
                col.label(text=f"Current: {action.name}")
                frame_range = f"{int(action.frame_range[0])}-{int(action.frame_range[1])}"
                col.label(text=f"Frames: {frame_range}")
            else:
                col.label(text="No Active Action", icon='ERROR')
        
        # Animation Export Options
        export_options_box = anim_box.box()
        export_options_box.label(text="Animation Options", icon='EXPORT')
        
        col = export_options_box.column()
        col.prop(props, "export_all_keys")
        col.prop(props, "use_frame_range")
        
        if props.use_frame_range:
            row = col.row(align=True)
            row.prop(props, "frame_start")
            row.prop(props, "frame_end")
        
        # Animation Export Button
        row = anim_box.row()
        row.scale_y = 2.0
        
        # Check if export is possible
        can_export = True
        error_msg = ""
        
        if not obj:
            can_export = False
            error_msg = "No active object"
        elif obj.type != 'MESH':
            can_export = False
            error_msg = "Object is not a mesh"
        elif not obj.data.shape_keys:
            can_export = False
            error_msg = "No shape keys"
        elif props.use_active_action:
            if not (obj.animation_data and obj.animation_data.action):
                can_export = False
                error_msg = "No active action"
        else:
            if props.selected_action == "NONE":
                can_export = False
                error_msg = "No action selected"
        
        if can_export:
            row.operator("udo.export_blendshape", icon='EXPORT', text="Export Animation JSON")
        else:
            row.enabled = False
            row.operator("udo.export_blendshape", icon='ERROR', text=f"Export ({error_msg})")
        
