import os
import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.Point import Point
import pyqtgraph.examples
# pyqtgraph.examples.run()
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 


class LabVisualizer():

    def __init__(self, mode: int = 0, *args):
        if mode == 0:
            self.init_as_static_1(*args)
        else:
            pass

    def init_as_static_1(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        self.slice_lenght = 512
        # generate layout
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('pyqtgraph example: crosshair')
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        self.upper_wind = self.win.addPlot(row=1, col=0)  # window with original and processed signals
        self.middle_wind = self.win.addPlot(row=2, col=0)  # fft plot of slice lower_win
        self.lower_win = self.win.addPlot(row=3, col=0)  # window with processed signal and slice selector

        self.region = pg.LinearRegionItem()
        self.region.setZValue(0)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.lower_win.addItem(self.region, ignoreBounds=True)

        # pg.dbg()
        self.upper_wind.setAutoVisible(y=True)

        self.upper_wind.plot(self.data1, pen="r")
        self.upper_wind.plot(self.data2, pen="g")
        # p1.plot(data2, pen="g")

        self.lower_win.plot(self.data2, pen="w")
        self.region.sigRegionChanged.connect(self.update)
        self.upper_wind.sigRangeChanged.connect(self.updateRegion)

        self.region.setRegion([1000, 2000])

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.upper_wind.addItem(self.vLine, ignoreBounds=True)
        self.upper_wind.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.upper_wind.vb
        self.proxy = pg.SignalProxy(self.upper_wind.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        # p1.scene().sigMouseMoved.connect(mouseMoved)

    def update(self):
        self.region.setZValue(self.slice_lenght)
        minX, maxX = self.region.getRegion()
        self.upper_wind.setXRange(minX, maxX, padding=0)

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        pos = evt[0]  # using signal proxy turns original arguments into a tuple
        if self.upper_wind.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(self.data1):
                self.label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), self.data1[index], self.data2[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())


if __name__ == "__main__":
    sweep, tsweep = audiogenerator.generateSweptSine(amp=0.5,
                                                     f0=150,
                                                     f1=10000,
                                                     duration=1.0,
                                                     fs=44100,
                                                     fade=True,
                                                     novak=True)

    visualizer = LabVisualizer(0, tsweep, sweep)
    # Start Qt event loop unless running in interactive mode or using pyside.
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
