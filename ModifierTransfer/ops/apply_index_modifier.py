import bpy
from .. import utils


class OBJECT_OT_mt_apply_modifier_by_index(bpy.types.Operator):
    bl_idname = "object.mt_apply_modifier_by_index"
    bl_label = "Apply Modifier by Index"
    bl_description = "Apply the modifier at the given 1-based index on each selected object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = getattr(scene, 'mt_props', None)
        if props is None:
            self.report({'ERROR'}, "Props not found")
            return {'CANCELLED'}

        idx_1 = int(props.modifier_index)
        if idx_1 < 1:
            self.report({'WARNING'}, "Index must be >= 1")
            return {'CANCELLED'}
        idx0 = idx_1 - 1

        targets = list(context.selected_objects)
        if not targets:
            self.report({'INFO'}, "No selected objects")
            return {'CANCELLED'}

        applied = 0
        skipped = 0
        for obj in targets:
            mods = obj.modifiers
            if idx0 >= len(mods):
                skipped += 1
                continue
            mod = mods[idx0]
            ok = utils.safe_apply_modifier(obj, mod.name)
            if ok:
                applied += 1
            else:
                skipped += 1

        self.report({'INFO'}, f"Applied: {applied}, Skipped: {skipped}")
        return {'FINISHED'}
