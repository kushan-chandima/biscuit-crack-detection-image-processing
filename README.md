# Biscuit Crack Detection (Traditional Image Processing)

This application detects surface cracks in biscuits using traditional image processing techniques (no deep learning required). It works in real-time with live video and also supports image uploads.

## Features
- Real-time crack detection from webcam (selectable input source)
- Crack overlay in red on detected regions
- Status label: "Crack Detected" or "No Crack Detected"
- Upload images for crack detection
- Simple PyQt5 user interface

## Requirements
- Python 3.7+
- PyQt5
- OpenCV
- numpy

## Setup
1. Create and activate the virtual environment:
   ```
   python -m venv virtual-env-TRADITIONAL
   virtual-env-TRADITIONAL\Scripts\activate  # On Windows
   ```
2. Install dependencies:
   ```
   pip install pyqt5 opencv-python numpy
   ```
3. Run the application:
   ```
   python crack_detection_app.py
   ```

## Usage
- Select the camera source from the dropdown.
- View live detection results.
- Click "Upload Image" to analyze a photo.

## Notes
- The virtual environment folder (`virtual-env-TRADITIONAL/`) is excluded from git.
- For best results, use a plain background and good lighting.

---

Feel free to fork, modify, and contribute!
