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
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crack_found = False
    overlay = image.copy()
    for cnt in contours:
        length = cv2.arcLength(cnt, False)
        if length > 40:  # Threshold for crack length
            crack_found = True
            cv2.drawContours(overlay, [cnt], -1, (0, 0, 255), 2)
    return overlay, crack_found

class CrackDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Biscuit Crack Detection')
        self.setGeometry(100, 100, 900, 700)
        self.video_label = QLabel()
        self.status_label = QLabel('Status: No video')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.upload_image)
        self.camera_select = QComboBox()
        self.camera_select.currentIndexChanged.connect(self.change_camera)
        self.available_cameras = list_cameras()
        for idx in self.available_cameras:
            self.camera_select.addItem(f'Camera {idx}', idx)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel('Select Camera:'))
        top_layout.addWidget(self.camera_select)
        top_layout.addWidget(self.upload_btn)
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)
        container = QWidget()
        container.setLayout(layout)
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
                else:
                    self.status_label.setText('No Crack Detected')
            else:
                self.status_label.setText('Failed to read frame')

    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))

    def upload_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image files (*.jpg *.jpeg *.png *.bmp)')
        if fname:
            img = cv2.imread(fname)
            if img is not None:
                overlay, crack_found = detect_cracks(img)
                self.display_image(overlay)
                if crack_found:
                    self.status_label.setText('Crack Detected in Image!')
                else:
                    self.status_label.setText('No Crack Detected in Image')
            else:
                self.status_label.setText('Failed to load image')

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrackDetectionApp()
    window.show()
    sys.exit(app.exec_())
