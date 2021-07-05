import signal
import sys
from revised_main_window import BuoPrototype
from PyQt5.QtWidgets import QApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)

app = QApplication(sys.argv)
win = BuoPrototype()
win.show()
app.exec_()
