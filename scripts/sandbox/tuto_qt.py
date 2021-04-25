import sys
import os
import random
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene
from PySide6.QtCore import QFile, Qt, QRect, QPointF, QRectF, QSizeF
from PySide6.QtGui import QPen
from ui_tuto import Ui_widget
from ui_main import Ui_main
import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

sys.path.append(os.getcwd())
from lib import audiogenerator


class MyCanvas(FigureCanvas):
    def __init__(self, parent=None, axes=None):
        fig = matplotlib.figure.Figure()
        if axes is None:
            self.axes = fig.add_subplot(111)
            matplotlib.pyplot.subplots_adjust(0, 0, 1, 1, 0, 0)
        else:
            self.axes = fig.add_axes(axes)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        # self.fig, self.ax = plt.subplots(1, 1)
        self.generate_random_sine()

    def resize_axes(self, axes):
        self.axes.cla()
        self.axes.set_axis_off()
        self.axes = self.figure.add_axes(axes)

    def generate_random_sine(self):
        f_sine = random.randint(100, 10000)
        self.vect, self.signal = audiogenerator.generateSine(f0=f_sine)
        self.axes.plot(self.vect, self.signal)
        self.draw()


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
        self.ui.visualizer.scene = QGraphicsScene(QRect(10, 10, 771, 451))
        self.ui.visualizer.setScene(self.ui.visualizer.scene)
        self.ui.visualizer.pen = QPen(Qt.green)
        self.ui.visualizer.canvas = MyCanvas()
        # self.update_visualizer()

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
        self.update_visualizer()

    ##################
    # ON CLICK METHODS
    ##################

    def update_visualizer(self):
        self.ui.visualizer.canvas.generate_random_sine()
        to_draw = (QRectF(self.ui.visualizer.canvas.signal), QSizeF(20, 20))
        self.ui.visualizer.scene.addRect(to_draw, self.ui.visualizer.pen)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    my_mw = MyMainWindow()
    my_mw.show()
    # my_widget = MyWidget()
    # my_widget.show()

    sys.exit(app.exec_())
