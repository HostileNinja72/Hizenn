import sys 
import time

from PySide6.QtCore import QTimer, QRunnable, QThreadPool
from PySide6.QtWidgets import(QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,)

class Worker(QRunnable):
      def run(self):
            print("Thread start")
            time.sleep(5)
            print("Complete")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        print(
            "Multithreading with maximum %d threads" % self.
            threadpool.maxThreadCount()
        )

        self.message = ""
        self.count = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("Danger!")
        b.pressed.connect(self.oh_no)

        c = QPushButton("?")
        c.pressed.connect(self.change_message)

        layout.addWidget(self.l)
        layout.addWidget(b)

        layout.addWidget(c)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()


        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
    
    def recurring_timer(self):
        self.count += 1
        self.l.setText("Counter %d" % self.count)


    def change_message(self):
            self.message = "OH NO"

    def oh_no(self):
            worker = Worker()
            self.threadpool.start(worker)

            for _ in range(100):
                time.sleep(0.1)
                self.l.setText(self.message)
                QApplication.processEvents()

app = QApplication(sys.argv)
window = MainWindow()
app.exec()