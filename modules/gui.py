import sys
# import random
# from PySide6 import QtCore, QtWidgets, QtGui
# from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtCore import QFile, QIODevice

from ui_lab import Ui_MainWindow

class MyWidget(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.buttn = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

class MyLabUiWidget():
    def __init__(self):
        self.ui_file_name = "modules\lab.ui"
        self.ui_file = QFile(self.ui_file_name)
        if not self.ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {self.ui_file_name}: {self.ui_file.errorString()}")
            sys.exit(-1)

        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()
        if not self.window:
            print(self.loader.errorString())
            sys.exit(-1)

class MyGui():
    def __init__(self):
        self.main_widget = MyLabUiWidget()
        self.second_widget = MyWidget()
        self.main_widget.window.show()
        self.second_widget.layout.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow
        self.ui.setupUi(self, MainWindow)


if __name__ == "__main__":
    # app = QtWidgets.QApplication([])

    app = QApplication(sys.argv)
    # window = MyGui()
 
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
