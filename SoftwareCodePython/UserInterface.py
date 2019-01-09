#coding:utf-8
#
# pip install pyqt5
# pip install pyqt5-tools
# python configure.py

# Developer: Deiner Zapata Silva
# Proyecto: DelBot (DALC)

import sys

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# Importando librerias propias
import VoiceBot as vb
import EventClass as ec
##############################################################################################################
class App(QMainWindow): #QWidget
 
    def __init__(self):
        super().__init__()
        self.title = 'DelBot'
        self.left = 100
        self.top = 100
        self.width = 280
        self.height = 70

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initUI()
        #Configuración de voz - DelBot
        self.delbot=vb.VoiceBot()
        self.delbot.speak("Hola soy Delbot")
        self.delbot.enable(True)
        
        self.catchEvent = ec.EventClass()
    def initUI(self):
        # Barra de edicion
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')
        
        #
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Configuración de botones
        bHight=30
        bWidth=80
        dX = 10
        dY = 30

        button = QPushButton('RECORD', self)
        button.setToolTip('Inicia la captura de movimientos del usuario')
        button.resize(bWidth,bHight)
        button.move(10,dY) 
        button.clicked.connect(self.on_click_record)

        button = QPushButton('STOP', self)
        button.setToolTip('Detiene la captura de movimientos del usuario')
        button.resize(bWidth,bHight)
        button.move(100,dY)
        button.clicked.connect(self.on_click_stop)

        button = QPushButton('PLAY', self)
        button.setToolTip('Reproduce la captura de movimientos del usuario')
        button.resize(bWidth,bHight)
        button.move(190,dY) 
        button.clicked.connect(self.on_click_play)

        """
        #buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if( buttonReply==QMessageBox.Yes):
            print("YES CLICKED")
        else:
            print("NO CLICKED")
        """
        self.show()
 
    @pyqtSlot()
    def on_click_play(self):
        self.delbot.speak("Repitiendo movimientos")
        self.catchEvent.playMovUser()
    
    @pyqtSlot()
    def on_click_stop(self):
        self.delbot.speak("Deteniendo captura")
        self.catchEvent.stopWatchDogUser()
        self.catchEvent.stopWatchDogScreen()
        
    @pyqtSlot()
    def on_click_record(self):
        self.delbot.speak("Capturando movimientos")
        #self.catchEvent.runWatchDogUser()
        self.catchEvent.runWatchDogScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
