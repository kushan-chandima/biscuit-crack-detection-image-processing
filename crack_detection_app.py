def contour_touches_border(cnt, img_shape, border_thresh=2):
    h, w = img_shape[:2]
    for pt in cnt:
        x, y = pt[0]
        if x <= border_thresh or x >= w - border_thresh - 1 or y <= border_thresh or y >= h - border_thresh - 1:
            return True
    return False
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

def list_cameras(max_cameras=5):
    # Try to open cameras 0..max_cameras-1 and return available indices
    available = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

def detect_cracks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crack_found = False
    overlay = image.copy()

    # Find the largest contour (likely the biscuit margin)
    largest = max(contours, key=cv2.contourArea) if contours else None

    for cnt in contours:
        if cnt is largest:
            continue  # Skip the margin
        area = cv2.contourArea(cnt)
        if area < 10:
            continue  # Ignore tiny noise
        # Optional: filter by circularity
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if circularity > 0.7:  # 1.0 is a perfect circle
            continue  # Likely not a crack
        length = cv2.arcLength(cnt, False)
        if length > 40 and not contour_touches_border(cnt, image.shape):
            crack_found = True
            cv2.drawContours(overlay, [cnt], -1, (0, 0, 255), 2)
    return overlay, crack_found

class CrackDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Biscuit Crack Detection')
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: #e3f0fa;")  # Light blue for better contrast

        # Title label
        title_label = QLabel('🍪 Biscuit Crack Detection')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333; margin: 20px 0 10px 0;")

        # Video display
        self.video_label = QLabel()
        self.video_label.setFixedSize(600, 400)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background: #fff; border: 2px solid #b0b0b0; border-radius: 16px; margin: 10px auto;")

        # Status label
        self.status_label = QLabel('Status: No video')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976d2; margin: 20px 0 10px 0;")

        # Upload button
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.setStyleSheet("padding: 8px 24px; font-size: 16px; background: #1976d2; color: white; border-radius: 8px;")
        self.upload_btn.clicked.connect(self.upload_image)

        # Camera select
        self.camera_select = QComboBox()
        self.camera_select.setStyleSheet("padding: 6px 12px; font-size: 16px; border-radius: 8px; background: #fff; border: 1px solid #b0b0b0;")

        self.timer = QTimer()  # Ensure timer is defined before any slot can use it
        self.timer.timeout.connect(self.update_frame)
        self.camera_select.blockSignals(True)
        self.available_cameras = list_cameras()
        for idx in self.available_cameras:
            self.camera_select.addItem(f'Camera {idx}', idx)
        self.camera_select.blockSignals(False)
        self.camera_select.currentIndexChanged.connect(self.change_camera)
        self.cap = None

        # Layouts
        top_layout = QHBoxLayout()
        cam_label = QLabel('Select Camera:')
        cam_label.setStyleSheet("font-size: 16px; margin-right: 8px;")
        top_layout.addWidget(cam_label)
        top_layout.addWidget(self.camera_select)
        top_layout.addStretch(1)
        top_layout.addWidget(self.upload_btn)
        top_layout.setSpacing(16)
        top_layout.setContentsMargins(20, 10, 20, 10)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.setContentsMargins(30, 20, 30, 20)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Start with first camera if available
        if self.available_cameras:
            self.open_camera(self.available_cameras[0])
        else:
            self.status_label.setText('No camera found')

    def open_camera(self, cam_index):
        # Ensure self.cap always exists
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(cam_index)
        if self.cap.isOpened():
            self.status_label.setText(f'Camera {cam_index} opened')
            self.timer.start(30)
        else:
            self.status_label.setText(f'Failed to open camera {cam_index}')

    def change_camera(self):
        idx = self.camera_select.currentIndex()
        if idx >= 0:
            cam_index = self.camera_select.itemData(idx)
            self.open_camera(cam_index)

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                overlay, crack_found = detect_cracks(frame)
                self.display_image(overlay)
                if crack_found:
                    self.status_label.setText('Crack Detected!')
                    self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #d32f2f; margin: 20px 0 10px 0;")
                else:
                    self.status_label.setText('No Crack Detected')
                    self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #388e3c; margin: 20px 0 10px 0;")
            else:
                self.status_label.setText('Failed to read frame')
                self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976d2; margin: 20px 0 10px 0;")

    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))

    def upload_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image files (*.jpg *.jpeg *.png *.bmp)')
        print(f"[DEBUG] Selected file: {fname}")
        if fname:
            img = cv2.imread(fname)
            if img is None:
                print("[ERROR] cv2.imread returned None. File may not exist or is not a valid image.")
                self.status_label.setText('Failed to load image')
                self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976d2; margin: 20px 0 10px 0;")
                return
            print(f"[DEBUG] Loaded image shape: {img.shape}")
            # Resize if too large for display
            max_dim = 800
            h, w = img.shape[:2]
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
                print(f"[DEBUG] Resized image to: {img.shape}")
            overlay, crack_found = detect_cracks(img)
            print(f"[DEBUG] Crack found: {crack_found}")
            self.display_image(overlay)
            if crack_found:
                self.status_label.setText('Crack Detected in Image!')
                self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #d32f2f; margin: 20px 0 10px 0;")
            else:
                self.status_label.setText('No Crack Detected in Image')
                self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #388e3c; margin: 20px 0 10px 0;")

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrackDetectionApp()
    window.show()
    sys.exit(app.exec_())
