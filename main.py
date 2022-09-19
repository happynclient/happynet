import sys
import random
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_statview import Window, createDeviceStatModel

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setSourceModel(createDeviceStatModel(window))
    window.show()
    sys.exit(app.exec_())
