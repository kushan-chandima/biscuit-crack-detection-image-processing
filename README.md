
# Biscuit Crack Detection (Traditional Image Processing)

This application provides real-time detection of surface cracks in biscuits using traditional image processing techniques (no deep learning required). It features a modern graphical user interface (GUI) built with PyQt5, allowing users to analyze both live video streams and uploaded images for cracks. The system is designed for quality control in food production, research, or educational purposes.

## Features
- **Real-time crack detection:** Analyze biscuits in live video from any connected webcam (selectable input source).
- **Crack visualization:** Detected cracks are highlighted with a red overlay directly on the video or image.
- **Status feedback:** The status label displays "Crack Detected" (bold red) or "No Crack Detected" (bold green) for instant, clear feedback.
- **Image upload support:** Upload and analyze static images for cracks using the same detection pipeline.
- **Modern user interface:** Clean, attractive PyQt5 GUI with styled widgets and responsive layout.
- **Robust error handling:** Handles camera selection, initialization, and image loading errors gracefully.
## How It Works

The application uses traditional image processing steps to detect cracks:
1. **Grayscale conversion and blurring** to reduce noise.
2. **Edge detection** (Canny) to find potential cracks.
3. **Morphological operations** to enhance crack-like features.
4. **Contour analysis** to filter out the biscuit margin and noise, focusing on likely cracks.
5. **Overlay and feedback**: Cracks are drawn in red, and the status label updates in real time.

The same detection logic is applied to both live video and uploaded images.
## Troubleshooting

- **No camera detected:** Ensure your webcam is connected and not in use by another application.
- **Image upload does not work:** Only standard image formats (JPG, PNG, BMP) are supported. Check the terminal for debug messages if detection fails.
- **Cracks not detected:** Detection parameters are tuned for typical biscuit cracks. If your cracks are not detected, you may need to adjust the detection thresholds in the code.
- **False positives:** Strong edges or shadows may sometimes be detected as cracks. Use a plain background and good lighting for best results.
## Contribution

Contributions are welcome! You can:
- Fork the repository and submit pull requests for improvements.
- Report issues or suggest features via GitHub Issues.
- Adapt the code for other types of surface defect detection.

## Requirements
- Python 3.7+
- PyQt5
- OpenCV
- numpy

## Setup
1. **Create and activate a virtual environment** (recommended):
   ```sh
   python -m venv virtual-env-TRADITIONAL
   # On Windows:
   virtual-env-TRADITIONAL\Scripts\activate
   # On macOS/Linux:
   source virtual-env-TRADITIONAL/bin/activate
   ```
2. **Install dependencies using requirements.txt:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```sh
   python crack_detection_app.py
   ```

## Usage
- Select the camera source from the dropdown.
- View live detection results. The status label turns bold red if a crack is detected, and bold green if not.
- Click "Upload Image" to analyze a photo.


## Notes
- The virtual environment folder (`virtual-env-TRADITIONAL/`) is excluded from git.
- For best results, use a plain background and good lighting.
- The application now handles camera and timer initialization bugs gracefully.
- All detection parameters are in `crack_detection_app.py` and can be tuned for your specific use case.

---

---

Feel free to fork, modify, and contribute! For questions or support, open an issue on GitHub.
