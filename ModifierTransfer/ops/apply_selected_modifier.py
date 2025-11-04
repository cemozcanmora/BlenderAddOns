import bpy
from .. import utils


class OBJECT_OT_mt_apply_selected_modifier(bpy.types.Operator):
    bl_idname = "object.mt_apply_selected_modifier"
    bl_label = "Copy/Apply Selected Modifier"
    bl_description = "Copy the chosen modifier from the active object to all selected objects; optionally apply"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = getattr(scene, 'mt_props', None)
        if props is None:
            self.report({'ERROR'}, "Props not found")
            return {'CANCELLED'}

        active = context.active_object
        if active is None:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        if not active.modifiers:
            self.report({'WARNING'}, "Active object has no modifiers")
            return {'CANCELLED'}

        sel_mod_name = props.selected_modifier
        if not sel_mod_name or sel_mod_name not in active.modifiers:
            self.report({'WARNING'}, "Selected modifier not found on active")
            return {'CANCELLED'}

        src_mod = active.modifiers[sel_mod_name]
        apply_now = bool(props.apply_immediately)

        # Operate on selected objects except the active (unless user also wants it?)
        targets = [obj for obj in context.selected_objects if obj != active]
        if not targets:
            self.report({'INFO'}, "No target objects selected")
            return {'CANCELLED'}

        applied = 0
        copied = 0
        for obj in targets:
            ok = utils.copy_modifier_to_object(obj, src_mod, apply_immediately=apply_now)
            if ok:
                if apply_now:
                    applied += 1
                else:
                    copied += 1

        msg = []
        if copied:
            msg.append(f"copied: {copied}")
        if applied:
            msg.append(f"applied: {applied}")
        self.report({'INFO'}, "; ".join(msg) if msg else "Nothing changed")
        return {'FINISHED'}
