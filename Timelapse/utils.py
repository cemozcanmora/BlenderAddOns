import bpy
import math
from mathutils import Vector

def get_object_bounds(obj):
    """Get the bounding box of an object in world space"""
    if obj is None:
        return None
    
    # Get bounding box corners in world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Calculate min and max for each axis
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    min_z = min(corner.z for corner in bbox_corners)
    max_z = max(corner.z for corner in bbox_corners)
    
    center = Vector((
        (min_x + max_x) / 2,
        (min_y + max_y) / 2,
        (min_z + max_z) / 2
    ))
    
    size = Vector((
        max_x - min_x,
        max_y - min_y,
        max_z - min_z
    ))
    
    return center, size

def position_camera_to_object(camera, target_obj, angle='PERSPECTIVE', distance_multiplier=2.5):
    """Position and orient camera to frame the target object"""
    
    if camera is None or target_obj is None:
        return
    
    # Get object bounds
    bounds = get_object_bounds(target_obj)
    if bounds is None:
        return
    
    center, size = bounds
    
    # Calculate the maximum dimension
    max_dimension = max(size.x, size.y, size.z)
    
    # Get camera data
    cam_data = camera.data
    
    # Calculate required distance based on camera FOV and object size
    if cam_data.type == 'PERSP':
        fov = cam_data.angle
        # Distance to fit object in frame
        distance = (max_dimension / 2) / math.tan(fov / 2) * distance_multiplier
    else:
        # Orthographic camera
        cam_data.ortho_scale = max_dimension * distance_multiplier
        distance = max_dimension * 2
    
    # Set camera position based on angle
    if angle == 'FRONT':
        offset = Vector((0, -distance, 0))
    elif angle == 'BACK':
        offset = Vector((0, distance, 0))
    elif angle == 'LEFT':
        offset = Vector((-distance, 0, 0))
    elif angle == 'RIGHT':
        offset = Vector((distance, 0, 0))
    elif angle == 'TOP':
        offset = Vector((0, 0, distance))
    else:  # PERSPECTIVE
        # 3/4 view angle
        offset = Vector((distance * 0.7, -distance * 0.7, distance * 0.5))
    
    camera.location = center + offset
    
    # Point camera at object center
    direction = center - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

def create_timelapse_scene(scene_name, target_obj, camera_angle='PERSPECTIVE', distance_multiplier=2.5):
    """Create a new scene with camera for timelapse"""
    
    # Create new scene
    timelapse_scene = bpy.data.scenes.new(scene_name)
    
    # Link the target object to the new scene
    if target_obj:
        timelapse_scene.collection.objects.link(target_obj)
    
    # Create camera
    camera_data = bpy.data.cameras.new(name=f"{scene_name}_Camera")
    camera_obj = bpy.data.objects.new(f"{scene_name}_Camera", camera_data)
    timelapse_scene.collection.objects.link(camera_obj)
    
    # Set as active camera
    timelapse_scene.camera = camera_obj
    
    # Position camera
    if target_obj:
        position_camera_to_object(camera_obj, target_obj, camera_angle, distance_multiplier)
    
    # Create a light for better visibility
    light_data = bpy.data.lights.new(name=f"{scene_name}_Light", type='SUN')
    light_data.energy = 2.0
    light_obj = bpy.data.objects.new(f"{scene_name}_Light", light_data)
    timelapse_scene.collection.objects.link(light_obj)
    light_obj.location = (5, -5, 10)
    light_obj.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Configure render settings for timelapse
    timelapse_scene.render.resolution_x = 1920
    timelapse_scene.render.resolution_y = 1080
    timelapse_scene.render.image_settings.file_format = 'PNG'
    
    return timelapse_scene, camera_obj

def update_camera_framing(camera, target_obj, distance_multiplier=2.5):
    """Update camera position to keep object framed"""
    
    if camera is None or target_obj is None:
        return
    
    bounds = get_object_bounds(target_obj)
    if bounds is None:
        return
    
    center, size = bounds
    max_dimension = max(size.x, size.y, size.z)
    
    # Get camera data
    cam_data = camera.data
    
    # Update distance based on object size
    if cam_data.type == 'PERSP':
        fov = cam_data.angle
        distance = (max_dimension / 2) / math.tan(fov / 2) * distance_multiplier
    else:
        cam_data.ortho_scale = max_dimension * distance_multiplier
        distance = max_dimension * 2
    
    # Maintain current direction but update distance
    current_direction = (camera.location - center).normalized()
    camera.location = center + (current_direction * distance)
    
    # Update camera rotation to look at center
    direction = center - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

def render_timelapse_frame(scene, output_path, frame_number):
    """Render a single frame for the timelapse"""
    
    # Store current scene
    original_scene = bpy.context.window.scene
    
    # Switch to timelapse scene
    bpy.context.window.scene = scene
    
    # Set output path
    scene.render.filepath = f"{output_path}frame_{frame_number:05d}"
    
    # Render
    bpy.ops.render.render(write_still=True)
    
    # Restore original scene
    bpy.context.window.scene = original_scene
