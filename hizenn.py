import sys
from PySide6.QtCore import Qt, QTimer,QSize
from PySide6.QtGui import QColor,QPixmap,QTransform
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMainWindow, QTabWidget, QLabel,QTabBar,QWidget
from ui.ui_splash_screen import Ui_SplashScreen
from Widgets import CircularProgress
from functions.cameraWidget import CameraWidget
from functions.videoUpload import VideoUploadWidget
from functions.imageUpload import ImageUploaderWidget
import tensorflow as tf
import qdarktheme
from qdarktheme.qtpy.QtCore import Qt
from qdarktheme.qtpy.QtGui import QIcon
from qdarktheme.qtpy.QtWidgets import (
    QLabel,
    QMainWindow,
    QSizePolicy,
)

class CustomTabBar(QTabBar):
    def tabSizeHint(self, index):
        size = super(CustomTabBar, self).tabSizeHint(index)
        if index == 3:  
            return QSize(size.width(), self.height() - 350)
        return size

class CustomTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(CustomTabWidget, self).__init__(*args, **kwargs)
        self.setTabBar(CustomTabBar())
        self.setTabPosition(QTabWidget.West)
        self.setDocumentMode(True)
        self.setMovable(True)

counter = 0

class SplashScreen(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Remove Title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.toggle = "dark"

        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 50
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)
        self.progress.font_size = 20
        self.progress.addShadow(True)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        self.show()

        # Add SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(self.shadow)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.previous_index = 0  # Initialize previous index to 0

    # Update progress bar
    def update(self):
        global counter

        # Set value to progress bar
        self.progress.setValue(counter)

        # Stop counter
        if counter >= 100:
            self.timer.stop()

            # Close Splash Screen and start the main app
            self.close()
            self.init()

        # Increases counter
        counter += 1

    def init(self):
        self.camera_widget = CameraWidget(self.toggle)
        self.video_upload_widget = VideoUploadWidget(self.toggle)
        self.image_upload_widget = ImageUploaderWidget()
        self.image_upload_widget.setTheme(self.toggle)
        self.video_upload_widget.setTheme(self.toggle,None)
        # Setup Widgets
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        empty_icon_pixmap = QPixmap(1, 100)
        empty_icon_pixmap.fill(Qt.transparent)
        empty_icon = QIcon(empty_icon_pixmap)

        button_tab = QLabel("",self)
        qdarktheme.setup_theme("auto")
        tab_widget.setIconSize(QSize(64,64))
        tab_widget.addTab(self.camera_widget,QIcon(QPixmap("images/camera.svg").transformed(QTransform().rotate(90))),"")
        tab_widget.addTab(self.video_upload_widget,QIcon(QPixmap("images/video.svg").transformed(QTransform().rotate(90))), "")
        tab_widget.addTab(self.image_upload_widget,QIcon(QPixmap("images/image.svg").transformed(QTransform().rotate(90))), "")
        tab_widget.addTab(spacer,empty_icon, "")
        tab_widget.addTab(button_tab,QIcon(QPixmap("images/light.svg").transformed(QTransform().rotate(90))),"")
        tab_widget.setTabEnabled(3, False)
        tab_widget.currentChanged.connect(self.handle_tab_changed)
        tab_widget.setStyleSheet("QTabBar::tab:hover {"
                                "    "
                                "}"
                                ""
                                "QTabBar::tab:selected{"
                                "    "
                                "}"
                                "QTabBar::tab {"	
                                "    margin: 0px;"
                                "}")
        tab_widget.setUsesScrollButtons=False
        tab_widget.resize(800, 600)
        tab_widget.show()

    def handle_tab_changed(self, index):
        if index == 4:
            if(self.toggle=="dark"):
                tab_widget.setTabIcon(4,QIcon(QPixmap("images/dark.svg").transformed(QTransform().rotate(90))))
                self.toggle="light"
            else:
                tab_widget.setTabIcon(4,QIcon(QPixmap("images/light.svg").transformed(QTransform().rotate(90))))
                self.toggle="dark"
            qdarktheme.setup_theme(self.toggle)
            self.camera_widget.setTheme(self.toggle)
            self.image_upload_widget.setTheme(self.toggle)
            self.video_upload_widget.setTheme(self.toggle,False)
            tab_widget.setCurrentIndex(self.previous_index)
        else:
            # Update the previous index with the new index
            self.previous_index = index

if __name__ == "__main__":
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.set_visible_devices(gpus[0], 'GPU')
            tf.config.experimental.set_memory_growth(gpus[0], True)
            print("GPU acceleration enabled.")
        except RuntimeError as e:
            print(e)
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    app.setApplicationName("Hizenn")
    app.setWindowIcon(QIcon("images/icon.png"))
    window = SplashScreen()
    tab_widget = CustomTabWidget()
    sys.exit(app.exec())
