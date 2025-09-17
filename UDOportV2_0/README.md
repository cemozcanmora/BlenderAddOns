# UDOport v2.0

A comprehensive Blender addon for Unity integration that combines FBX export capabilities with blendshape animation export functionality.

## Features

### FBX Export
- Export mesh, armature, and empty objects to Unity-optimized FBX format
- Automatic vertex group name cleaning (removes '_Parent' suffixes)
- Custom armature rotation handling for Unity compatibility
- Optional transform application before export
- Animation export toggle
- Object naming tools (remove numeric suffixes)

### Animation Export
- Export blendshape animations as JSON files for Unity
- Support for multiple actions (active or selected)
- Custom frame range support
- Option to export all shape keys (animated + non-animated)
- Real-time validation and error checking
- Unity-compatible JSON output format with keyframe data

## Installation

1. Copy the "UDOport v2.0" folder to your Blender addons directory:
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Linux: `~/.config/blender/[version]/scripts/addons/`

2. Enable the addon in Blender Preferences > Add-ons > Search for "UDOport"

## Usage

### FBX Export
1. Select the objects you want to export (mesh, armature, empty)
2. Open the UDOport panel in the 3D Viewport sidebar
3. Configure export options (animation, transforms)
4. Click "Export FBX to Unity"
5. Choose your export location

### Animation Export
1. Select a mesh object with shape keys
2. Ensure the object has an action with shape key animations
3. Configure animation export options in the UDOport panel
4. Click "Export Animation JSON"
5. Choose your export location

## JSON Output Format

The animation export creates Unity-compatible JSON files with the following structure:

```json
{
  "clip_name": "ActionName",
  "fps": 24,
  "frame_start": 1,
  "frame_end": 250,
  "duration": 10.42,
  "object_name": "ObjectName",
  "bindings": [
    {
      "path": "ObjectName",
      "property": "blendShape.ShapeKeyName",
      "keys": [
        {
          "time": 0.0,
          "value": 0.0,
          "interpolation": "BEZIER",
          "inTangent": [0.0, 0.0],
          "outTangent": [0.0, 0.0]
        }
      ]
    }
  ]
}
```

## Requirements

- Blender 4.4.0 or higher
- Objects with shape keys for animation export
- Actions with shape key keyframes for animation export

## Version History

### v2.0.0
- Combined UDOport and AnimationExporter functionality
- Unified UI panel with both FBX and animation export features
- Maintained all original features from both addons
- Improved organization and user experience
