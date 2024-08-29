#Project dependecies
import cv2
from deepface import DeepFace
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget



#Widget depedencies
from functions.cameraWidget import *
from functions.videoUpload import *
from functions.imageUpload import *

#UI depedencies
from ui.ui_splash_screen import Ui_SplashScreen
from Widgets.circular_progress import CircularProgress

