import signal
import sys
from buo_py_bindings import get_buo_output
from PyQt5.QtCore import QSize, QMetaObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,  QPushButton, QLabel, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QSizePolicy

signal.signal(signal.SIGINT, signal.SIG_DFL)


class BuoPrototype(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Buo Prototype')
        self.setFixedSize(QSize(560, 720))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        self.centralWidget().setLayout(central_layout)

        QMetaObject.connectSlotsByName(self)


app = QApplication(sys.argv)
win = BuoPrototype()
win.show()
app.exec_()
