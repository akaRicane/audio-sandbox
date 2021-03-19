import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import numpy as np
import os
sys.path.append(os.getcwd())
from modules import player as Player
from lib import audiodata, audiodsp


# DOCUMENTATION HERE ######
# import pyqtgraph.examples
# pyqtgraph.examples.run()
###########################


class LabVisualizer():

    def __init__(self, mode: int = 1, *args):
        if mode == 1:
            self.init_as_static_1(*args)
        elif mode == 2:
            self.init_as_static_2(*args)
        elif mode == 3:
            self.init_as_static_3(*args)
        elif mode == 10:
            self.init_as_dynamic_1(*args)
        else:
            pass

    def init_as_static_1(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        self.slice_lenght = 512
        # generate layout
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('static 1')
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        self.upper_wind = self.win.addPlot(row=1, col=0)  # window with original and processed signals
        self.middle_wind = self.win.addPlot(row=2, col=0)  # fft plot of slice lower_wind
        self.lower_wind = self.win.addPlot(row=3, col=0)  # window with processed signal and slice selector

        self.region = pg.LinearRegionItem()
        self.region.setZValue(0)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.upper_wind.addItem(self.region, ignoreBounds=True)

        # pg.dbg()
        self.upper_wind.setAutoVisible(y=True)

        self.upper_wind.plot(self.data1, pen="r")
        self.upper_wind.plot(self.data2, pen="g")
        # p1.plot(data2, pen="g")

        self.lower_wind.plot(self.data2, pen="g")
        self.region.sigRegionChanged.connect(self.update)
        self.lower_wind.sigRangeChanged.connect(self.updateRegion)

        self.region.setRegion([0, self.slice_lenght])

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.lower_wind.addItem(self.vLine, ignoreBounds=True)
        self.lower_wind.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.lower_wind.vb
        self.proxy = pg.SignalProxy(self.lower_wind.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        # p1.scene().sigMouseMoved.connect(mouseMoved)
        # Start Qt event loop unless running in interactive mode or using pyside.
        if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
            pg.QtGui.QApplication.exec_()

    def init_as_static_2(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        self.slice_lenght = 512
        # generate layout
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('static 2')
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        self.upper_wind = self.win.addPlot(row=1, col=0)  # window with original and processed signals
        self.lower_wind = self.win.addPlot(row=2, col=0)  # window with processed signal and slice selector

        self.upper_wind.setAutoVisible(y=True)

        self.upper_wind.plot(self.data1, pen="r")
        self.upper_wind.plot(self.data2, pen="g")

        self.lower_wind.plot(self.data2, pen="g")

        if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
            pg.QtGui.QApplication.exec_()

    def init_as_dynamic_1(self, data):
        # generate layout
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('dynamic 1')
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        self.rt_plot = self.win.addPlot(title="Updating plot")
        self.curve = self.rt_plot.plot(pen='y')
        # self.ptr = 0
        def run():
            self.curve.setData(data)
            # self.curve.setData(data[self.ptr % 10])
            # if self.ptr == 0:
            #     self.rt_plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            # self.ptr += 1
        timer = QtCore.QTimer()
        timer.timeout.connect(run)
        timer.start(5)
        if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
            pg.QtGui.QApplication.exec_()

    def init_as_static_3(self, data1, data2):
        pass
    #     self.data1 = data1
    #     self.data2 = data2
    #     self.slice_lenght = 512
    #     # generate layout
    #     self.app = QtGui.QApplication([])
    #     self.win = pg.GraphicsLayoutWidget(show=True)
    #     self.win.setWindowTitle('static 3')
    #     # LABEL
    #     self.label = pg.LabelItem(justify='right')
    #     self.win.addItem(self.label)
    #     # PLOT
    #     self.upper_wind = self.win.addPlot(row=1, col=0)  # window with original and processed signals
    #     self.lower_wind = self.win.addPlot(row=2, col=0)  # window with processed signal and slice selector
    #     self.upper_wind.setAutoVisible(y=True)
    #     self.upper_wind.plot(self.data1, pen="r")
    #     self.upper_wind.plot(self.data2, pen="g")
    #     self.lower_wind.plot(self.data2, pen="g")
    #     # TREE
    #     self.param = Parameter.create(name='Parameters', type='group', children=tree_architecture)
    #     # loop waiting modif in tree content
    #     self.param.sigTreeStateChanged.connect(self.change)
    #     self.param.sigValueChanging.connect(self.valueChanging)
    #     # create ParameterTree widget
    #     self.tree = ParameterTree()
    #     self.tree.setParameters(self.param, showTop=False)
    #     self.tree.setWindowTitle('pyqtgraph example: Parameter Tree')

    #     if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
    #         pg.QtGui.QApplication.exec_()

    def create_region_item(self):
        pass

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


class SignalVisualizer():

    def __init__(self, buffer_size, rate, n_channels=1):
        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.chunk = audiodata.AudioData(rate=rate)
        self.chunk.fftsize = 512
        self.chunk.npts = buffer_size
        self.chunk.t = np.arange(0, buffer_size, n_channels)
        self.chunk.f = np.linspace(0, int(self.chunk.rate / 2), self.chunk.fftsize)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Spectrum Analyzer')
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1200, 800)

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        sp_xlabels = [
            (np.log10(10), '10'), (np.log10(100), '100'),
            (np.log10(1000), '1000'), (np.log10(22050), '22050')
        ]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
        self.spectrum = self.win.addPlot(
            title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},
        )
        self.win.show()

    def start(self):
        # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #     QtGui.QApplication.instance().exec_()
        self.app.exec_()

    def set_plotdata(self, name, data_x, data_y):
        if len(data_y) != len(data_x):
            # zero padding du pauvre
            size_missing = int((len(data_x) - len(data_y)) / 2)
            data_y = np.pad(data_y, size_missing).tolist()
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, self.chunk.npts, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.chunk.rate / 2), padding=0.005)

    def update(self, chunck):
        # self.chunk.rt_chunck_anaysis(chunck)
        self.set_plotdata(name='waveform', data_x=self.chunk.t, data_y=chunck)
        self.set_plotdata(name='spectrum', data_x=self.chunk.f, data_y=self.chunk.f)

    def animation(self, chunck):
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: self.update(chunck))
        timer.start(40)
