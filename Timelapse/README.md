# Timelapse Recorder for Blender

A Blender add-on that automatically creates timelapses while you work on objects, with dynamic camera positioning that adapts to object size changes.

## Features

- **Automatic Scene Creation**: Creates a dedicated timelapse scene with camera and lighting
- **Dynamic Camera Positioning**: Camera automatically adjusts to frame the object completely
- **Real-time Tracking**: Monitors object changes and updates framing dynamically
- **Multiple Camera Angles**: Choose from Front, Back, Left, Right, Top, or Perspective views
- **Automatic Capture**: Captures frames at regular intervals during modeling
- **Manual Control**: Option to capture frames manually when needed

## Installation

1. Download or clone this repository
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install" and select the Timelapse folder or zip file
4. Enable the "Timelapse Recorder" add-on

## Usage

### Basic Workflow

1. **Select Your Object**: Select the object you want to track in the 3D viewport
2. **Open the Panel**: Find the "Timelapse" tab in the sidebar (press N to toggle sidebar)
3. **Set Target**: The selected object will be set as the target automatically, or click "Use Active Object"
4. **Configure Settings**:
   - **Camera Angle**: Choose your preferred viewing angle
   - **Camera Distance**: Adjust how far the camera is from the object
   - **Auto Frame**: Keep enabled for automatic size adjustments
   - **Capture Interval**: How often to capture frames (lower = more frequent)
   - **Output Path**: Where to save timelapse frames
5. **Start Recording**: Click "Start Recording" button
6. **Work on Your Model**: Edit your object as normal - frames will be captured automatically
7. **Stop Recording**: Click "Stop Recording" when done

### Settings

#### Target Object
- **Target Object**: The object to track and frame in the timelapse
- **Use Active Object**: Quick button to set the currently selected object as target

#### Camera Settings
- **Camera Angle**: Choose viewing angle (Front, Back, Left, Right, Top, Perspective)
- **Camera Distance**: Multiplier for camera distance (1.0 = tight framing, higher = more space)
- **Auto Frame**: Automatically adjusts camera when object size changes
- **Update Camera**: Manually update camera position with current settings

#### Recording Settings
- **Interval Mode**: How to measure capture intervals
  - **Scene Updates**: Capture based on scene changes (depsgraph updates)
  - **Mouse Clicks**: Capture every N mouse clicks
  - **Keyboard Strokes**: Capture every N keyboard presses
  - **Any Input**: Capture every N mouse clicks or keyboard presses
- **Capture Interval**: Number of events between captures (clicks, keystrokes, or scene updates)
- **Output Path**: Directory where frames will be saved (default: //timelapse/)
- **Scene Name**: Name of the timelapse scene (default: Timelapse_Scene)

### Controls

- **Start Recording**: Begin automatic timelapse capture
- **Stop Recording**: Stop automatic capture
- **Capture Frame Now**: Manually capture a single frame
- **View Timelapse Scene**: Switch to the timelapse scene to see camera view
- **Reset Timelapse**: Stop recording and delete the timelapse scene

## Tips

1. **Interval Mode Selection**:
   - **Scene Updates**: Best for automated recording while modeling/sculpting (default behavior)
   - **Mouse Clicks**: Great for click-intensive workflows like placing objects or applying operations
   - **Keyboard Strokes**: Perfect for keyboard-heavy workflows (shortcuts, typing, etc.)
   - **Any Input**: Captures general activity, good for mixed workflows

2. **Capture Interval**: 
   - **Scene Updates mode**: Lower (1-5) = every change, Higher (10-50) = major changes only
   - **Mouse/Keyboard modes**: Lower (1-3) = frequent captures, Higher (5-20) = selective captures
   - Recommended starting values:
     - Scene Updates: 10
     - Mouse Clicks: 5
     - Keyboard Strokes: 5
     - Any Input: 10

3. **Camera Distance**: 
   - Increase if you're making the object much larger
   - Decrease for tighter framing on small objects

4. **Output Path**: 
   - Use `//` prefix for relative paths (relative to .blend file location)
   - Ensure the directory exists or will be created automatically

5. **Creating Final Video**:
   - Use Blender's Video Sequencer or external tools like FFmpeg
   - Example FFmpeg command:
     ```
     ffmpeg -framerate 30 -i frame_%05d.png -c:v libx264 -pix_fmt yuv420p timelapse.mp4
     ```

## Workflow Examples

### Example 1: Modeling a Character
1. Start with a base mesh
2. Select mesh and start timelapse recording
3. Model your character - frames capture automatically as you work
4. Stop recording when complete
5. Compile frames into video

### Example 2: Sculpting Session
1. Select your sculpt object
2. Set capture interval to 5 for more detailed capture
3. Choose "Perspective" angle for best viewing
4. Start recording and sculpt
5. Camera auto-adjusts as you add volume

### Example 3: Manual Control
1. Set up target object
2. Don't start automatic recording
3. Use "Capture Frame Now" button after each major change
4. Full control over what gets captured

## Technical Notes

- The add-on creates a separate scene to avoid interfering with your work
- Original scene remains untouched
- Camera and lighting are automatically configured
- Frames are rendered at 1920x1080 PNG by default
- Modify `utils.py` to change render settings

## Troubleshooting

**No frames being captured:**
- Check that recording is started (green indicator)
- Verify target object is set
- Make changes to the object to trigger updates
- Lower the capture interval

**Camera not framing object correctly:**
- Click "Update Camera" to manually refresh
- Adjust Camera Distance multiplier
- Try different camera angles
- Ensure Auto Frame is enabled

**Render is slow:**
- Increase capture interval to reduce frequency
- Use lower resolution (modify scene render settings)
- Switch to simpler materials during timelapse

## License

This add-on is provided as-is for use in your Blender projects.

## Version History

### v1.0.0
- Initial release
- Automatic scene creation
- Dynamic camera positioning
- Multiple camera angles
- Auto-framing for size changes
- Manual and automatic capture modes
