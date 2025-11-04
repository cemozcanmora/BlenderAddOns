# Animation Exporter - Blender Addon

A Blender addon for exporting blendshape (shape key) animations to JSON format for Unity integration.

## Features

- Export blendshape animations from Blender to Unity-compatible JSON format
- Choose from available actions on the active object
- Option to use active action or select from all available actions
- Custom frame range support
- Export all shape keys (animated and non-animated)
- Comprehensive UI with real-time validation
- Detailed animation information display

## Installation

1. Copy the `AnimationExporter` folder to your Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - **Linux**: `~/.config/blender/[version]/scripts/addons/`

2. Open Blender and go to `Edit > Preferences > Add-ons`

3. Search for "Animation Exporter" and enable the addon

4. The panel will appear in the 3D Viewport sidebar under the "Animation Export" tab

## Usage

### Prerequisites

1. Select a mesh object with shape keys
2. Ensure the object has an action with keyframed shape key animations
3. The shape key animations should use the standard Blender format: `key_blocks["ShapeKeyName"].value`

### Export Process

1. **Select Object**: Choose a mesh object with shape keys in the 3D viewport

2. **Choose Action**:
   - Enable "Use Active Action" to export the currently active action
   - Or disable it and select from the dropdown list of available actions

3. **Configure Options**:
   - **Export All Shape Keys**: Include non-animated shape keys with constant values
   - **Use Frame Range**: Override action frame range with custom start/end frames

4. **Export**: Click the "Export Blendshape Animation" button and choose your save location

### JSON Output Format

The exported JSON file contains:

```json
{
  "clip_name": "ActionName",
  "fps": 24,
  "frame_start": 1,
  "frame_end": 100,
  "duration": 4.166667,
  "object_name": "CharacterHead",
  "bindings": [
    {
      "path": "CharacterHead",
      "property": "blendShape.EyeBlink_L",
      "keys": [
        {
          "time": 0.0,
          "value": 0.0,
          "interpolation": "BEZIER",
          "inTangent": [0.0, 0.0],
          "outTangent": [0.041667, 0.5]
        },
        {
          "time": 0.041667,
          "value": 1.0,
          "interpolation": "BEZIER",
          "inTangent": [-0.041667, -0.5],
          "outTangent": [0.041667, -0.5]
        },
        {
          "time": 0.083333,
          "value": 0.0,
          "interpolation": "LINEAR",
          "inTangent": [-0.041667, 0.5],
          "outTangent": [0.0, 0.0]
        }
      ]
    }
  ]
}
```

### Unity Integration

The JSON format is designed for Unity's Animation system:

- `path`: GameObject hierarchy path
- `property`: Blendshape property in format `blendShape.ShapeKeyName`
- `keys`: Array of keyframe objects with detailed interpolation data

#### Keyframe Data Structure

Each keyframe contains:
- `time`: Time in seconds
- `value`: Blendshape weight value (0.0 to 1.0)
- `interpolation`: Blender interpolation mode (`CONSTANT`, `LINEAR`, `BEZIER`)
- `inTangent`: Left handle tangent as `[time_offset, value_offset]`
- `outTangent`: Right handle tangent as `[time_offset, value_offset]`

#### Blender to Unity Interpolation Mapping

- **CONSTANT**: Step interpolation (no smoothing)
- **LINEAR**: Linear interpolation between keyframes
- **BEZIER**: Smooth interpolation using tangent handles

The tangent data allows Unity to recreate the exact curve shape from Blender, preserving easing and custom curve modifications.

## Troubleshooting

### Common Issues

1. **"No shape keys" error**: Ensure your mesh has shape keys created
2. **"No active action" error**: Create an action and add keyframes to shape key values
3. **Empty export**: Verify that shape keys are actually keyframed in the action
4. **Missing shape keys**: Check that shape key names match between Blender and your expectations

### Validation

The addon performs real-time validation and will show error messages for:
- No active object selected
- Selected object is not a mesh
- Object has no shape keys
- No action available or selected

## Technical Details

### Shape Key Animation Detection

The addon looks for F-Curves with data paths matching the pattern:
```
key_blocks["ShapeKeyName"].value
```

### Frame Rate Conversion

Keyframe times are converted from Blender frames to seconds using:
```
time_seconds = frame_number / scene_fps
```

### Supported Blender Versions

- Blender 3.0 and newer
- Tested with Blender 3.x and 4.x

## License

This addon is provided as-is for educational and production use.
