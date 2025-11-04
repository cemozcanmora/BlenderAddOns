import bpy


class VIEW3D_PT_mt_modifier_transfer(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Modifier Transfer'
    bl_label = 'Modifier Transfer'

    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH', 'SCULPT', 'POSE'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = getattr(scene, 'mt_props', None)

        col = layout.column(align=True)
        col.label(text="Copy from Active:")
        row = col.row(align=True)
        row.prop(props, 'selected_modifier', text="Modifier")
        col.prop(props, 'apply_immediately')
        col.operator('object.mt_apply_selected_modifier', icon='MODIFIER')

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Batch Apply by Index:")
        row = col.row(align=True)
        row.prop(props, 'modifier_index')
        col.operator('object.mt_apply_modifier_by_index', icon='CHECKMARK')
