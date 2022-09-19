import sys
import random
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
from netcat import createDeviceStatModel
from ui_statview import Window

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setClientModel(createDeviceStatModel(window))
    window.setServerModel(createDeviceStatModel(window))
    window.show()
    sys.exit(app.exec_())
