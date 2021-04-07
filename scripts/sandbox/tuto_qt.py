import sys
import os
import random
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene
from PySide6.QtCore import QFile, Qt, QRect, QPointF
from PySide6.QtGui import QPen
from ui_tuto import Ui_widget
from ui_main import Ui_main
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audiogenerator


class MyCanvas():
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.generate_random_sine()
        # plt.show(False)

    def generate_random_sine(self):
        f_sine = random.randint(100, 10000)
        self.signal = audiogenerator.generateSine(f0=f_sine)
        self.ax = plt.plot(*self.signal)
        # self.ax.draw()
        # self.fig.draw()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.ui = Ui_widget()
        self.ui.setupUi(self)
        self.setWindowTitle("My App")
        self.connectSignalsSlots()
        # self.show()

    def connectSignalsSlots(self):
        self.ui.button.clicked.connect(self.hello)

    def hello(self):
        input_text = self.ui.input.toPlainText()
        self.ui.output.setText(f'Hello {input_text}')


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.setWindowTitle("My Main Window")
        self.mywidget = MyWidget()
        self.build_visualizer()
        self.connectSignalsSlots()

    def build_visualizer(self):
        self.ui.visualizer.setScene(QGraphicsScene())
        self.ui.visualizer.pen = QPen(Qt.green)
        self.ui.visualizer.canvas = MyCanvas()

    def connectSignalsSlots(self):
        self.ui.btn_run_widget.clicked.connect(self.on_click_run_widget)
        self.ui.btn_run_analysis.clicked.connect(self.on_click_run_analysis)

    ##################
    # ON CLICK METHODS
    ##################

    def on_click_run_widget(self):
        self.ui.output_log.setText('Running widget ...')
        self.mywidget.show()

    def on_click_run_analysis(self):
        self.ui.output_log.setText('Running analysis ...')

    ##################
    # ON CLICK METHODS
    ##################

    def update_visualizer(self):
        draw = QRectF(QPointF(i*side, j*side), QtCore.QSizeF(side, side))
        scene.addRect(r, pen)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    my_mw = MyMainWindow()
    my_mw.show()
    # my_widget = MyWidget()
    # my_widget.show()

    sys.exit(app.exec_())
