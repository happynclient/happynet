import sys
import random
import time
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_statview import Window


class UpdateThread(QtCore.QThread):
    update_date = QtCore.Signal(str)

    def run(self):
        cnt = 0
        while True:
            cnt += 1
            self.update_date.emit(str(cnt))
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    update_thread = UpdateThread()
    update_thread.update_date.connect(window.updateClientModel)
    update_thread.start()
    #window.updateClientModel()
    window.show()
    sys.exit(app.exec_())
