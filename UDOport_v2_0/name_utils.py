import bpy
import re
from bpy.types import Operator
from bpy.props import StringProperty

class UDO_OT_RemoveNumericSuffixes(Operator):
    """Remove numeric suffixes from selected objects, handling naming conflicts"""
    bl_idname = "object.remove_numeric_suffixes"
    bl_label = "Remove Numeric Suffixes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        # Get all object names in the scene to check for conflicts
        all_objects = {obj.name: obj for obj in bpy.data.objects}
        
        # First pass: collect all target names and handle conflicts
        rename_map = {}  # {object: new_name}
        temp_renames = {}  # {object: temp_name}
        objects_to_restore = {}  # {object: original_name}
        
        # First, identify all objects that need renaming
        for obj in context.selected_objects:
            if not obj.name:
                continue
                
            # Check if name ends with .### pattern
            match = re.match(r'^(.*?)(\.\d+)?$', obj.name)
            if not match or not match.group(2):
                continue
                
            base_name = match.group(1)
            rename_map[obj] = base_name
            
            # Check if the base name is already taken by an object not in our selection
            if base_name in all_objects and all_objects[base_name] not in context.selected_objects:
                existing_obj = all_objects[base_name]
                # Create a temporary name for the existing object
                temp_name = f"{base_name}_temp"
                counter = 1
                while temp_name in all_objects or temp_name in temp_renames.values():
                    temp_name = f"{base_name}_temp_{counter}"
                    counter += 1
                temp_renames[existing_obj] = temp_name
                objects_to_restore[existing_obj] = base_name
        
        # Store original names for all objects we'll be touching
        all_affected = {**{obj: obj.name for obj in rename_map}, 
                       **{obj: obj.name for obj in temp_renames}}
        
        try:
            # First, rename conflicting objects to temporary names
            for obj, temp_name in temp_renames.items():
                try:
                    obj.name = temp_name
                except Exception as e:
                    self.report({'WARNING'}, f"Could not rename {obj.name} to {temp_name}: {str(e)}")
                    # Remove from our maps if we can't rename
                    if obj in temp_renames:
                        del temp_renames[obj]
                    if obj in objects_to_restore:
                        del objects_to_restore[obj]
            
            # Then rename our target objects
            success_count = 0
            for obj, new_name in list(rename_map.items()):
                try:
                    obj.name = new_name
                    success_count += 1
                except Exception as e:
                    self.report({'WARNING'}, f"Could not rename {obj.name} to {new_name}: {str(e)}")
                    if obj in rename_map:
                        del rename_map[obj]
            
            # Finally, restore the original objects to their base names
            for obj, original_name in objects_to_restore.items():
                try:
                    if obj.name.startswith(original_name + '_temp'):
                        obj.name = original_name
                except Exception as e:
                    self.report({'WARNING'}, f"Could not restore {obj.name} to {original_name}: {str(e)}")
            
            if success_count > 0:
                self.report({'INFO'}, f"Successfully renamed {success_count} objects")
            else:
                self.report({'WARNING'}, "No objects were renamed")
            return {'FINISHED'}
            
        except Exception as e:
            import traceback
            error_msg = f"Error during renaming: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            
            # Try to restore all original names
            for obj, original_name in all_affected.items():
                try:
                    if hasattr(obj, 'name') and obj.name != original_name:
                        obj.name = original_name
                except Exception as restore_error:
                    print(f"Failed to restore {obj.name if hasattr(obj, 'name') else 'object'}: {str(restore_error)}")
            
            self.report({'ERROR'}, f"Error during renaming: {str(e)}")
            return {'CANCELLED'}

def clean_vertex_group_names(objects, report_callback=None):
    """
    Remove '_Parent' suffix from all vertex groups in the given objects
    
    Args:
        objects: List of Blender objects to process
        report_callback: Optional function to report progress (e.g., self.report for operators)
    
    Returns:
        int: Number of vertex groups that were renamed
    """
    cleaned_count = 0
    
    for obj in objects:
        if obj.type != 'MESH' or not obj.vertex_groups:
            continue
            
        for vg in obj.vertex_groups:
            original_name = vg.name
            # Remove '_Parent' suffix specifically, preserving underscores before R/L suffixes
            cleaned_name = re.sub(r'_parent(?=_[RL]|$)', '', original_name, flags=re.IGNORECASE)
            # Clean up any double underscores that might result
            cleaned_name = cleaned_name.replace('__', '_').strip('_')
            
            if cleaned_name != original_name:
                # Check if the cleaned name already exists
                if cleaned_name in obj.vertex_groups and cleaned_name != original_name:
                    if report_callback:
                        report_callback({'WARNING'}, 
                                     f"Could not rename '{original_name}' to '{cleaned_name}': name already exists")
                    continue
                    
                # Store the original name for reference
                vg.name = cleaned_name
                cleaned_count += 1
                print(f"Renamed vertex group: '{original_name}' -> '{cleaned_name}' in object '{obj.name}'")
    
    if cleaned_count > 0 and report_callback:
        report_callback({'INFO'}, f"Removed '_Parent' suffix from {cleaned_count} vertex groups")
        print(f"\n=== Cleaned {cleaned_count} vertex group names ===\n")
    
    return cleaned_count
