import cv2
import mediapipe as mp
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap,QPainter, QColor
from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel,QHBoxLayout
from fer import FER
from PySide6.QtCharts import QChart, QChartView, QPieSeries

class CameraWidget(QWidget):
    def __init__(self,darkmode):
        super().__init__()


        self.camera_button = QPushButton("Turn Camera On")
        self.camera_button.clicked.connect(self.toggle_camera)

        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        

        self.cap = None

        #INIT FER DETECTOR
        self.detector = FER()

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.camera_button)
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        self.data = QPieSeries()

        self.chart = QChart()
        if darkmode=="dark":
            self.chart.setBackgroundBrush(QColor(30, 30, 30))
            self.chart.setTitleBrush(QColor(255, 255, 255))
        else:
            self.chart.setBackgroundBrush(QColor(255, 255, 255))
            self.chart.setTitleBrush(QColor(30, 30, 30))
        self.chart.addSeries(self.data)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        window_width = self._chart_view.width()
        window_height = self._chart_view.height()
        
        # Calculate the font size based on the window size
        font_size = min(window_width, window_height) // 30  # Adjust the division factor as desired
        
        # Set the font size for the chart title
        font = self.chart.titleFont()
        font.setPointSize(font_size)
        self.chart.setTitleFont(font)
        self.chart.setTitle('Detected Emotion :')

        data_layout = QVBoxLayout()
        data_layout.addWidget(self._chart_view)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.display_frame)

        toplayout = QHBoxLayout(self)
        toplayout.addLayout(layout)
        toplayout.addLayout(data_layout)
        toplayout.setStretch(0, 3)
        toplayout.setStretch(1, 1)

        self.setLayout(toplayout)

    def setTheme(self,darkmode):
        if darkmode=="dark":
            self.chart.setBackgroundBrush(QColor(30, 30, 30))
            self.chart.setTitleBrush(QColor(255, 255, 255))
        else:
            self.chart.setBackgroundBrush(QColor(255, 255, 255))
            self.chart.setTitleBrush(QColor(30, 30, 30))

    @QtCore.Slot()
    def toggle_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                no_camera_pixmap = QPixmap("images/off.svg")
                self.image_label.setPixmap(no_camera_pixmap)
                text = "<html><body><img src='images/off.svg' style='display:block;margin:auto;'><br>No camera detected</body></html>"
                self.image_label.setText(text)
                self.camera_button.setText("Turn Camera Off")
                return
            self.camera_button.setText("Turn Camera Off")
            self.timer.start(30)
        else:
            self.cap.release()
            self.cap = None
            self.camera_button.setText("Turn Camera On")
            self.timer.stop()
            self.image_label.clear()
    
    def update_chart_title(self, emotion):
        color = self.get_emotion_color(emotion)[0]
        emoji = self.get_emotion_color(emotion)[1]

        title = "<div style='text-align: center;'>"
        title += "<div style='font-weight: bold; font-size: 18px;'>Detected Emotion:</div>"
        title += "<div style='color: {0}; font-size: 24px;'>{1}</div>".format(color, emotion)
        title += "<div style='font-size: 36px;'>{0}</div>".format(emoji)
        title += "</div>"

        self.chart.setTitle(title)

    @QtCore.Slot()
    def display_frame(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return

        # Perform frame analysis
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image_height, image_width, _ = frame_rgb.shape
    
        # Detect faces using Mediapipe
        results = self.mp_face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * image_width), int(bbox.ymin * image_height), \
                             int(bbox.width * image_width), int(bbox.height * image_height)
                emotion, _ = self.detector.top_emotion(frame_rgb)
                emotion_color = self.get_emotion_color(emotion)[0]
                self.data.clear()
                emotions = {}
                if self.detector.detect_emotions(frame_rgb):
                    emotions = self.detector.detect_emotions(frame_rgb)[0]['emotions']
                for e, value in emotions.items():
                    slice = self.data.append(e, value)
                    color = self.get_emotion_color(e)[0]
                    slice.setColor(QColor(*color))
                    
                    if slice.label() == emotion:
                        slice.setExploded(True)
                    else:
                        slice.setExploded(False)
                    self.update_chart_title(emotion)
                for slice in self.data.slices():
                    slice.setLabelVisible(True)
                    
                cv2.putText(frame_rgb, text=(emotion), org=(x, y - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                                fontScale=1, color=emotion_color, thickness=2)
                cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), color=emotion_color, thickness=2)

        image = QImage(
            frame_rgb, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))


    def get_emotion_color(self, emotion):
        if emotion == "angry":
            return [(255, 0, 0),"🤬"]  # Red
        elif emotion == "happy":
            return [(0, 255, 0),"😁"]   # Green
        elif emotion == "sad":
            return [(0, 0, 255),"😢"]   # Blue
        elif emotion == "surprise":
            return [(255, 255, 0),"😮"]  # Yellow
        elif emotion == "neutral":
            return [(200, 200, 200),"😐"]   # White
        elif emotion == "disgust":
            return [(0, 0, 0),"🤢"]  # Black
        elif emotion == "fear":
            return [(200,100,50),"😨"] # idk 
        else:
            return [(0, 0, 0),""]  # Black

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        event.accept()