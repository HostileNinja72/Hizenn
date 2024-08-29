import cv2
import mediapipe as mp
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QApplication,QHBoxLayout
from PySide6.QtGui import QImage, QPixmap,QPainter,QColor
from PySide6.QtCore import QThread, Signal,Qt
from PIL import Image
from clip_interrogator import Config, Interrogator
import tensorflow as tf
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from fer import FER
import csv



class ImageUploaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        
        #INIT FER DETECTOR
        self.detector = FER(mtcnn=True)

        self.setWindowTitle('Image Uploader')
        layout = QVBoxLayout()
        self.emotions=[]

        self.image_label = QLabel(self)
        text = "<html><body><img src='images/upload.svg' style='display:block;margin:auto;'><br>Upload an Image</body></html>"
        self.image_label.setText(text)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.text_label = QLabel(self)
        self.text_label.setWordWrap(True)
        layout.addWidget(self.text_label)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.uploadImage)
        layout.addWidget(self.upload_button)
        
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        self.data = QPieSeries()

        self.chart = QChart()

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

        self.export = QPushButton("Export Data")
        self.export.clicked.connect(self.exportEmotions)
        self.export.setEnabled(False)

        data_layout = QVBoxLayout()
        data_layout.addWidget(self._chart_view)
        data_layout.addWidget(self.export)

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

    def uploadImage(self):
        self.upload_button.setEnabled(False)
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, 'Upload Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        if image_path:
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            image = Image.open(image_path).convert('RGB')
            self.display_frame(image_path)
            self.updateProgress(20)
            self.interrogation_thread = InterrogationThread(image)
            self.interrogation_thread.progressChanged.connect(
                self.updateProgress)
            self.interrogation_thread.resultObtained.connect(
                self.updateTextLabel)
            self.interrogation_thread.start()
        self.upload_button.setEnabled(True)
        self.export.setEnabled(True)

    def updateProgress(self, progress):
        self.progress_bar.setValue(progress)
        QApplication.processEvents()

    def updateTextLabel(self, result):
        self.text_label.setText(result)

    def convert_cv2_to_qimage(self,cv2_img):
        height, width, channel = cv2_img.shape
        bytes_per_line = channel * width
        return QImage(cv2_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
    
    def exportEmotions(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, 'Export Emotions Data', '', 'CSV Files (*.csv)')
        if file_path:
            self.exportEmotionsData(file_path)
    
    def exportEmotionsData(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Emotion', 'Value'])
            for emotion, value in self.emotions.items():
                writer.writerow([emotion, value])

    def display_frame(self, image_path):
        img=cv2.imread(image_path)
        image_height, image_width, _ = img.shape
        if img is None:
        # Failed to load the image, handle the error
            return
        results = self.mp_face_detection.process(img)
        if results.detections:
            bbox = results.detections[0].location_data.relative_bounding_box
            x, y, w, h = int(bbox.xmin * image_width), int(bbox.ymin * image_height), \
                             int(bbox.width * image_width), int(bbox.height * image_height)
            output = self.detector.detect_emotions(img)
            emotion, _ = self.detector.top_emotion(img)
            emotion_color = self.get_emotion_color(emotion)[0]
            self.data.clear()
            self.emotions = output[0]['emotions']
            for e, value in self.emotions.items():
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

            cv2.putText(img, text=(emotion), org=(x, y - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                                    fontScale=1, color=emotion_color, thickness=2)
            cv2.rectangle(img, (x, y), (x + w, y + h), color=emotion_color, thickness=2)
        # Set the QPixmap in the QLabel
        q_image = self.convert_cv2_to_qimage(img)
        self.image_label.setPixmap(QPixmap.fromImage(q_image))

    def get_emotion_color(self, emotion):
        if emotion == "angry":
            return [(255, 0, 0), "🤬"]  # Red
        elif emotion == "happy":
            return [(0, 255, 0), "😁"]  # Green
        elif emotion == "sad":
            return [(0, 0, 255), "😢"]  # Blue
        elif emotion == "surprise":
            return [(255, 255, 0), "😮"]  # Yellow
        elif emotion == "neutral":
            return [(255, 255, 255), "😐"]  # White
        elif emotion == "disgust":
            return [(0, 0, 0), "🤢"]  # Black
        elif emotion == "fear":
            return [(200,100,50),"😨"] # idk 
        else:
            return [(0, 0, 0), "❓"]  # Black, default emoji for unrecognized emotion

    def update_chart_title(self, emotion):
        color = self.get_emotion_color(emotion)[0]
        emoji = self.get_emotion_color(emotion)[1]

        title = "<div style='text-align: center;'>"
        title += "<div style='font-weight: bold; font-size: 18px;'>Detected Emotion:</div>"
        title += "<div style='color: {0}; font-size: 24px;'>{1}</div>".format(color, emotion)
        title += "<div style='font-size: 36px;'>{0}</div>".format(emoji)
        title += "</div>"

        self.chart.setTitle(title)

class InterrogationThread(QThread):
    progressChanged = Signal(int)
    resultObtained = Signal(str)

    def __init__(self, image):
        super().__init__()
        self.image = image

    def run(self):
        # Configure TensorFlow GPU memory growth
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("GPU memory growth enabled.")
            except RuntimeError as e:
                print(e)

        # Use the first GPU for TensorFlow operations
        with tf.device('/GPU:0'):
            ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
            self.progressChanged.emit(80)
            result = ci.interrogate(self.image)

        self.progressChanged.emit(100)  # Signal completionn
        self.resultObtained.emit(result)  # Emit the result obtained
