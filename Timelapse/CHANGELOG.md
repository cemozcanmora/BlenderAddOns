# Changelog

All notable changes to the Timelapse Recorder add-on will be documented in this file.

## [1.1.0] - 2024-11-01

### Added
- **Interval Mode Selection**: Choose how to measure capture intervals
  - Scene Updates: Based on depsgraph updates (original behavior)
  - Mouse Clicks: Capture every N mouse clicks
  - Keyboard Strokes: Capture every N keyboard presses
  - Any Input: Capture on any mouse click or keyboard press
- Modal event tracker operator for capturing user input events
- Event counter display in UI for input-based modes
- Contextual interval labels in UI based on selected mode

### Changed
- Default interval mode is now "Mouse Clicks" instead of scene updates
- Default capture interval reduced to 5 (from 10) for better granularity with input events
- Depsgraph handler now only activates in Scene Updates mode
- Improved UI with mode-specific labels and feedback

## [1.0.0] - 2024-11-01

### Added
- Initial release of Timelapse Recorder add-on
- Automatic timelapse scene creation with dedicated camera and lighting
- Dynamic camera positioning that frames objects automatically
- Real-time object tracking with automatic framing adjustments
- Multiple camera angle presets (Front, Back, Left, Right, Top, Perspective)
- Configurable capture intervals for automatic frame capture
- Manual frame capture option
- Auto-frame feature that responds to object size changes
- Adjustable camera distance multiplier
- Custom output path configuration
- Scene viewing and navigation tools
- Reset functionality to clean up timelapse data
- Comprehensive UI panel in 3D viewport sidebar
- Depsgraph update handler for real-time monitoring
- Automatic render configuration (1920x1080 PNG)

### Features
- **Operators**:
  - Start/Stop Recording
  - Capture Frame (manual)
  - View Timelapse Scene
  - Update Camera
  - Reset Timelapse
  - Set Active Object as Target
  
- **Properties**:
  - Target object selection
  - Camera angle selection
  - Camera distance multiplier
  - Auto-frame toggle
  - Capture interval
  - Output path
  - Scene name customization
  
- **Utilities**:
  - Object bounding box calculation
  - Camera positioning algorithms
  - Dynamic framing updates
  - Scene creation and management
  - Frame rendering system

### Technical Details
- Compatible with Blender 4.0+
- Non-intrusive design (separate scene for timelapse)
- Efficient depsgraph monitoring
- World-space bounding box calculations
- Support for both perspective and orthographic cameras
