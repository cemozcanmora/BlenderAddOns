import bpy
from typing import Optional


def set_active_object(obj: bpy.types.Object) -> bpy.types.Object:
    """Set the given object as active, return previous active to restore later."""
    view_layer = bpy.context.view_layer
    prev_active = view_layer.objects.active
    view_layer.objects.active = obj
    return prev_active


def ensure_selected(obj: bpy.types.Object):
    obj.select_set(True)


def ensure_object_mode() -> str:
    """Ensure we are in OBJECT mode. Return previous mode to restore later."""
    prev_mode = None
    obj = bpy.context.active_object
    try:
        prev_mode = obj.mode if obj else None
    except Exception:
        prev_mode = None
    try:
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass
    return prev_mode or 'OBJECT'


def restore_mode(prev_mode: str):
    try:
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode=prev_mode)
    except Exception:
        pass


def safe_apply_modifier(obj: bpy.types.Object, mod_name: str) -> bool:
    """Apply a modifier by name on the given object, returns success."""
    if obj is None or mod_name not in obj.modifiers:
        return False
    prev_active = set_active_object(obj)
    prev_mode = ensure_object_mode()
    ensure_selected(obj)
    try:
        bpy.ops.object.modifier_apply(modifier=mod_name)
        return True
    except Exception:
        return False
    finally:
        # Restore active
        bpy.context.view_layer.objects.active = prev_active
        restore_mode(prev_mode)


def make_unique_modifier_name(obj: bpy.types.Object, base: str) -> str:
    name = base
    i = 1
    existing = {m.name for m in obj.modifiers}
    while name in existing:
        i += 1
        name = f"{base}.{i:03d}"
    return name


def add_modifier_like(obj: bpy.types.Object, src_mod: bpy.types.Modifier) -> Optional[bpy.types.Modifier]:
    """Create a new modifier on obj with the same type and similar settings as src_mod.
    Attempts to copy RNA properties when possible.
    """
    try:
        new_name = make_unique_modifier_name(obj, src_mod.name)
        dst = obj.modifiers.new(name=new_name, type=src_mod.type)
    except Exception:
        return None

    # Copy simple properties
    try:
        rna = src_mod.bl_rna
        for prop in rna.properties:
            if prop.is_readonly or prop.identifier in {"name", "type", "rna_type"}:
                continue
            pid = prop.identifier
            try:
                setattr(dst, pid, getattr(src_mod, pid))
            except Exception:
                # Some properties are pointers or collections not directly assignable; ignore
                pass
    except Exception:
        pass

    return dst


def copy_modifier_to_object(target_obj: bpy.types.Object, src_mod: bpy.types.Modifier, apply_immediately: bool = False) -> bool:
    """Copy src_mod to target_obj and optionally apply it. Returns success."""
    dst = add_modifier_like(target_obj, src_mod)
    if not dst:
        return False
    if apply_immediately:
        return safe_apply_modifier(target_obj, dst.name)
    return True
