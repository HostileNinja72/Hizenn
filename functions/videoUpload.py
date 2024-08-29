from PySide6 import QtCore, QtMultimedia
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPainter,QColor
from PySide6.QtWidgets import QFileDialog,QApplication, QVBoxLayout, QWidget, QPushButton, QSlider, QProgressBar,QHBoxLayout,QLabel
from PySide6.QtMultimediaWidgets import QVideoWidget
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QThread, Signal
from PySide6.QtCharts import QChart, QChartView, QPieSeries
import cv2
import mediapipe as mp
from clip_interrogator import Config, Interrogator
from fer import FER
from PIL import Image
import os
import tensorflow as tf
from functions.frameWidget import FrameListWidget
import torch
import csv

class VideoUploadWidget(QWidget):
    frame_analyzed = Signal(str, dict, int)
    def __init__(self,darkmode):
        super().__init__()
        self.frame_analyzed.connect(self.create_chart)
        self.dark=darkmode
        self.initUI()
        
    def initUI(self):

        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        
        #INIT FER DETECTOR
        self.detector = FER(mtcnn=True)

        self.cap = None

        layout = QVBoxLayout()

        self.frame_old_list = []

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.video_label = QVideoWidget()
        self.video_player = QtMultimedia.QMediaPlayer(self)
        self.video_player.setVideoOutput(self.video_label)
        text = "<html><body><img src='images/upload.svg' style='display:block;margin:auto;'><br>Upload a Video</body></html>"
        self.image_label.setText(text)
        layout.addWidget(self.image_label)
        layout.addWidget(self.video_label)
        self.video_label.hide()

        self.frame_list_widget = FrameListWidget()
        self.frame_list_widget.setFixedHeight(150)
        layout.addWidget(self.frame_list_widget)
        self.frame_list_widget.hide()

        self.desc_label = QLabel(self)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        self.desc_label.hide()

        self.play_button = QPushButton("Pause")
        self.play_button.clicked.connect(self.play_pause_video)
        self.play_button.clicked.connect(self.hide_frame_list_widget)
        layout.addWidget(self.play_button)
        self.play_button.hide()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setEnabled(False)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.sliderMoved.connect(self.update_frame_index)
        self.slider.sliderMoved.connect(self.preview_frame)

        self.video_player.positionChanged.connect(self.update_frame_index)
        self.video_player.positionChanged.connect(self.enableInterrogation)
        layout.addWidget(self.slider)
        self.slider.hide()

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.interrogate_button = QPushButton("Interrogate")
        self.interrogate_button.setEnabled(False)
        self.interrogate_button.clicked.connect(self.interrogatestuff)
        layout.addWidget(self.interrogate_button)

        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        self.datas = []

        self.edata = QPieSeries()

        self.chart = QChart()

        self.chart.addSeries(self.edata)

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

        self.interrogation_thread = None
        self.paused_frame = None

        self.setLayout(toplayout)

    def hide_frame_list_widget(self):
        if self.frame_list_widget and self.frame_list_widget.isVisible():
            self.frame_list_widget.hide()

    def enableInterrogation(self,toggle):
        self.interrogate_button.setEnabled(toggle)

    def exportEmotions(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, 'Export Emotions Data', '', 'CSV Files (*.csv)')
        if file_path:
            self.exportEmotionsData(file_path)

    def exportEmotionsData(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Frame', 'Emotion', 'Value'])
            for chart in self.datas:
                frame = chart.chart_index
                slices = chart.series()[0].slices()
                largest_slice = max(slices, key=lambda slice: slice.value())
                emotion = largest_slice.label() if largest_slice else ''
                value = len(slices)
                writer.writerow([frame, emotion, value])



    @QtCore.Slot(int)
    def update_frame_index(self, position):
        # Calculate current frame index based on the position of the slider
        total_frames = len(self.frame_list)
        self.current_frame_index = int((position / self.slider.maximum()) * total_frames)
        qimage = self.frame_old_list[self.current_frame_index]
        self.paused_frame = self.convert_qimage_to_pil(qimage)
        # Show the chart corresponding to the current frame index
        if self.current_frame_index < len(self.datas):
            self._chart_view.setChart(self.datas[self.current_frame_index])

    def preview_frame(self):
        if self.frame_list_widget:    
            self.frame_list_widget.scroll_to_frame(self.current_frame_index)
            qimage = self.frame_old_list[self.current_frame_index]
            self.paused_frame = self.convert_qimage_to_pil(qimage)
            if not self.frame_list_widget.isVisible():
                self.frame_list_widget.show()
        
    def setTheme(self,darkmode,charts):
        if darkmode=="dark":
            self.chart.setBackgroundBrush(QColor(30, 30, 30))
            self.chart.setTitleBrush(QColor(255, 255, 255))
            if charts:
                charts.setBackgroundBrush(QColor(30, 30, 30))
                charts.setTitleBrush(QColor(255, 255, 255))
        else:
            self.chart.setBackgroundBrush(QColor(255, 255, 255))
            self.chart.setTitleBrush(QColor(30, 30, 30))
            if charts:
                charts.setBackgroundBrush(QColor(255, 255, 255))
                charts.setTitleBrush(QColor(30, 30, 30))


    @QtCore.Slot()
    def upload_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video files (*.mp4 *.avi);;All files (*.*)")

        if file_dialog.exec_():
            self.upload_button.setEnabled(False)
            self.datas=[]
            self.desc_label.setText("")
            self.file_path = file_dialog.selectedFiles()[0]
            media_url = QUrl.fromLocalFile(self.file_path)
            self.video_player.setSource(media_url)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.video_player.duration())
            self.slider.setEnabled(True)
            self.video_player.positionChanged.connect(self.update_slider_position)
            self.video_player.durationChanged.connect(self.update_slider_range)
            self.slider.sliderReleased.connect(self.hide_frame_list_widget)
            self.analyze()
            self.upload_button.setEnabled(True)
            self.export.setEnabled(True)

    def update_slider_position(self, position):
        self.slider.setValue(position)

    def updateProgress(self, progress):
        if (self.progress_bar.value()+progress > 100):
            self.progress_bar.setValue(progress)
        else: 
            self.progress_bar.setValue(self.progress_bar.value() + progress)
        QApplication.processEvents()

    def update_slider_range(self, duration):
        self.slider.setMaximum(duration)

    def set_position(self, position):
        self.video_player.play()
        self.video_player.pause()
        self.play_button.setText("Play")
        self.video_player.setPosition(position)

    def convert_qimage_to_pil(self,qimage):
        rgb_frame = cv2.cvtColor(qimage, cv2.COLOR_BGR2RGB)

        # Create a PIL image from the converted frame
        pil_image = Image.fromarray(rgb_frame)
        return pil_image

    def play_pause_video(self):
        if self.video_player.isPlaying():
            self.video_player.pause()
            self.play_button.setText("Play")
            self.interrogate_button.setEnabled(True)
            qimage = self.frame_old_list[self.current_frame_index]
    
            self.paused_frame = self.convert_qimage_to_pil(qimage)
           
        else:
            self.video_player.play()
            self.play_button.setText("Pause")
            self.interrogate_button.setEnabled(False)
            self.paused_frame = None

        

    def closeEvent(self, event):
        self.video_player.stop()
        event.accept()
    
    def analyze_frame(self, frame, current_frame, total_frames):
        # Perform frame analysis
        self.frame_old_list.append(frame.copy())
        image_height, image_width, _ = frame.shape
        # Detect faces using Mediapipe
        results = self.mp_face_detection.process(frame)

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * image_width), int(bbox.ymin * image_height), \
                    int(bbox.width * image_width), int(bbox.height * image_height)
                emotion, _ = self.detector.top_emotion(frame)
                emotions = {}
                if self.detector.detect_emotions(frame):
                    emotions = self.detector.detect_emotions(frame)[0]['emotions']
                    val = (current_frame * 100) / total_frames
                    self.updateProgress(val)

                # Draw rectangles and text on the frame
                emotion_color = self.get_emotion_color(emotion)[0]
                cv2.putText(frame, text=emotion, org=(x, y - 20), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                            fontScale=1, color=(emotion_color[2], emotion_color[1], emotion_color[0]))
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              color=(emotion_color[2], emotion_color[1], emotion_color[0]), thickness=2)

                # Emit the frame_analyzed signal with the required data
                self.frame_analyzed.emit(emotion, emotions, current_frame)

        self.frame_list.append((frame, current_frame))
        current_frame += 1
        QtCore.QMetaObject.invokeMethod(self, "updateProgress", Qt.QueuedConnection, QtCore.Q_ARG(int, val))


    @QtCore.Slot(str, dict, int)
    def create_chart(self, emotion, emotions, chart_index):
        # Create a new chart for each frame
        torch.cuda.empty_cache()
        chart = QChart()
        data = QPieSeries()
        chart.addSeries(data)
        chart.setAnimationOptions(QChart.NoAnimation)

        # Set the font size for the chart title
        font = self.chart.titleFont()
        chart.setTitleFont(font)
        chart.setTitle("Detected Emotion:")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        for e, value in emotions.items():
            slice = data.append(e, value)
            color = self.get_emotion_color(e)[0]
            slice.setColor(QColor(*color))

            if slice.label() == emotion:
                slice.setExploded(True)
            else:
                slice.setExploded(False)
            self.setTheme(self.dark, chart)
            self.update_chart_title(emotion, chart)

        chart.chart_index = chart_index
        self.datas.append(chart)

        # Use invokeMethod to update the GUI in the main thread
        QtCore.QMetaObject.invokeMethod(self, "_update_chart_view", Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, chart_index))
        
    @QtCore.Slot(int)
    def _update_chart_view(self, chart_index):
        # Sort the chart list based on chart index
        self.datas.sort(key=lambda x: x.chart_index)

        # Show the chart corresponding to the current frame index
        if chart_index < len(self.datas):
            self._chart_view.setChart(self.datas[chart_index])

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
            return [(200, 200, 200), "😐"]  # White
        elif emotion == "disgust":
            return [(0, 0, 0), "🤢"]  # Black
        elif emotion == "fear":
            return [(200,100,50),"😨"] # idk 
        else:
            return [(0, 0, 0), "❓"]  # Black, default emoji for unrecognized emotion
        
    def update_chart_title(self, emotion,chart):
        color = self.get_emotion_color(emotion)[0]
        emoji = self.get_emotion_color(emotion)[1]

        title = "<div style='text-align: center;'>"
        title += "<div style='font-weight: bold; font-size: 18px;'>Detected Emotion:</div>"
        title += "<div style='color: {0}; font-size: 24px;'>{1}</div>".format(color, emotion)
        title += "<div style='font-size: 36px;'>{0}</div>".format(emoji)
        title += "</div>"

        chart.setTitle(title)

    def analyze(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.file_path)
        if not self.cap.isOpened():
            print("not opened")
            return

        self.frame_list = []  # Reset frame list
        self.frame_old_list = [] # Reset old frame list
        current_frame = 0  # Reset frame list
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0  # Reset frame list

        with ThreadPoolExecutor() as executor:
            while True:
                    ret, frame = self.cap.read()
                    if not ret or frame is None:
                        break
                    # Submit frame analysis task to the executor
                    executor.submit(self.analyze_frame, frame, current_frame, total_frames)
                    current_frame += 1
            # Wait for all analysis tasks to complete
            # Sort the frame list based on frame numbers
            executor.shutdown()
        self.frame_list.sort(key=lambda x: x[1])
        self.frame_list_widget.display_frames(self.frame_old_list)
            

        # Merge analyzed frames into a video
        if self.frame_list:
            output_file = "output_video.avi"
            frame_height, frame_width, _ = self.frame_list[0][0].shape
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(output_file, fourcc,
                                  30.0, (frame_width, frame_height))
            for frame, _ in self.frame_list:
                out.write(frame)
            out.release()

            # Play the resulting video
            self.image_label.hide()
            self.video_label.show()
            self.slider.show()
            self.play_button.show()
            media_url = QUrl.fromLocalFile(os.path.abspath(output_file))
            self.video_player.setSource(media_url)
            self.video_player.play()
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.video_player.duration())
            self.slider.setEnabled(True)
            self.video_player.positionChanged.connect(self.update_slider_position)
            self.video_player.durationChanged.connect(self.update_slider_range)
            self.updateProgress(100)

    def interrogatestuff(self):
        image = self.paused_frame
        if image:
            self.upload_button.setEnabled(False)
            self.interrogate_button.setEnabled(False)
            self.play_button.setEnabled(False)
            self.slider.setEnabled(False)
            self.export.setEnabled(False)
            self.interrogation_thread = InterrogationThread(image)
            self.interrogation_thread.progressChanged.connect(
                self.updateProgress)
            self.interrogation_thread.resultObtained.connect(
                self.updateTextLabel)
            self.interrogation_thread.setEnable.connect(
                self.setStuffEnabled
            )
            self.interrogation_thread.start()
        else:
            self.updateTextLabel("no image detected")

    def setStuffEnabled(self,isEnabled):
        self.upload_button.setEnabled(isEnabled)
        self.interrogate_button.setEnabled(isEnabled)
        self.play_button.setEnabled(isEnabled)
        self.slider.setEnabled(isEnabled)
        self.export.setEnabled(isEnabled)
        
    def updateTextLabel(self,result):
        self.desc_label.setText(result)
        self.desc_label.show()

class InterrogationThread(QThread):
    progressChanged = Signal(int)
    resultObtained = Signal(str)
    setEnable = Signal(bool)

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
            self.progressChanged.emit(1)
            ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
            self.progressChanged.emit(80)
            result = ci.interrogate(self.image)

        self.progressChanged.emit(19)  # Signal completion
        self.resultObtained.emit(result)  # Emit the result obtained
        self.setEnable.emit(True)