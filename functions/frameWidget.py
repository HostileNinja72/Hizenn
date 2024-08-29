from PySide6.QtWidgets import QLabel, QHBoxLayout, QMainWindow, QScrollArea, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QSize
import cv2

class FrameListWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_frame_index = 0

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    # Hide vertical scrollbar

        self.scroll_area.setFixedHeight(150)

        self.frame_widget = QWidget()
        self.frame_layout = QHBoxLayout(self.frame_widget)
        self.frame_layout.setAlignment(Qt.AlignLeft)

        self.scroll_area.setWidget(self.frame_widget)
        self.setCentralWidget(self.scroll_area)

        self.frame_label = QLabel()  # Create the frame label
        self.frame_layout.addWidget(self.frame_label)  # Add it to the layout

    def display_frames(self,frame_list):
        # Clear existing image widgets
        while self.frame_layout.count():
            item = self.frame_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        for frame in frame_list:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_label = QLabel()
            image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
            thumbnail_size = QSize(150, 150)  # Set the desired thumbnail size
            scaled_image = image.scaled(thumbnail_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)
            image_label.setPixmap(pixmap)
            self.frame_layout.addWidget(image_label)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.show_previous_frame()
        elif event.key() == Qt.Key_Right:
            self.show_next_frame()
        else:
            super().keyPressEvent(event)

    def show_previous_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
        self.update_frame_label()

    def scroll_to_frame(self, value):
        self.current_frame_index = value
        frame_widget = self.frame_widget.layout().itemAt(self.current_frame_index).widget()
        frame_position = frame_widget.pos().x()
        self.scroll_area.horizontalScrollBar().setValue(frame_position)


    def show_next_frame(self):
        if self.current_frame_index < len(self.frame_list) - 1:
            self.current_frame_index += 1
        self.update_frame_label()

    def update_frame_label(self):
        frame, _ = self.frame_list[self.current_frame_index]
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.frame_label.setPixmap(pixmap)
