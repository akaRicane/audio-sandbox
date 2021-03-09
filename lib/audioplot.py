import matplotlib.pyplot as plt
import numpy as np
import logging


class SignalVisualizer():
    """ Displays a couple of audio signal and their fft 
    """
    def __init__(self, t: list, tamp: list, f: list, famp: list):
        self.fig, (self.ax, self.ax2) = plt.subplots(2, figsize=(15, 8))
        self.t = t
        self.tamp = tamp
        self.f = f
        self.famp = famp

        self.init_lines()
        self.init_axes()

    def init_lines(self):
        self.line, = self.ax.plot(self.t, np.random.rand(len(self.tamp)), '-', lw=2)
        self.line2, = self.ax2.plot(self.f, np.random.rand(len(self.famp)), '-', lw=2)

    def init_axes(self):
        self.ax.set_title("AUDIO WAVEFORM")
        self.ax.set_xlabel("t [sec]")
        self.ax.set_ylabel("Magnitude")
        self.ax.set_xlim(self.t[0], self.t[-1])
        self.ax.set_ylim(-1, 1)
        plt.setp(self.ax,
                 xticks=[0, int(len(self.t) / 2), len(self.t)],
                 yticks=[min(self.tamp), max(self.tamp)])

        self.ax2.set_title("Spectral Content")
        self.ax2.set_xlabel("frequencies [Hz]")
        self.ax2.set_ylabel("Magnitude")
        self.ax2.set_xlim(self.f[0], self.f[-1])
        self.ax2.set_ylim(-1, 1)
        plt.setp(self.ax2,
                 xticks=[0, len(self.f)],
                 yticks=[min(self.famp), max(self.famp)])

    def show(self):
        plt.show()

    def populate_plot(self, data_line, data_line2):
        self.line.set_ydata(data_line)
        self.line2.set_ydata(data_line2)


def shortPlot(vect, data, space='time', scale='lin',
              isNormalizedAxis: bool = False):
    """Allows to plot multiple plots in one fig with some specific treatment

    Args:
        vect ([type]): [x axis]
        data ([type]): [y axis]
        space (str, optional): [time/spectral plot]. Defaults to 'time'
        scale (str, optional):
            [linear/semilog(x)/loglog plot]. Default to 'lin'
        isNormalizedAxis (bool, optional):
            [use 0:1 axis for normalized axis plots]. Default to None
    """
    plt.gcf()
    plt.ylabel("Magnitude")
    if scale == 'semilog':
        if not isinstance(data[0], list):
            plt.semilogx(vect, data) if len(data) < len(vect) else plt.semilogx(vect[:len(data)], data)  # noqa E501
        else:
            [plt.semilog(vect[:len(data[channel])], data[channel]) for channel in range(len(data))]  # noqa E501

    elif scale == 'loglog':
        if not isinstance(data[0], list):
            plt.loglog(vect, data) if len(data) < len(vect) else plt.loglog(vect[:len(data)], data)  # noqa E501
        else:
            [plt.loglog(vect[:len(data[channel])], data[channel]) for channel in range(len(data))]  # noqa E501

    else:  # scale == 'lin' or other
        if not isinstance(data[0], list):
            plt.plot(vect, data) if len(data) > len(vect) else plt.plot(vect[:len(data)], data)  # noqa E501
        else:
            [plt.plot(vect[:len(data[channel])], data[channel]) for channel in range(len(data))]  # noqa E501

    if space == 'time':
        plt.xlabel("Time [s]")
        plt.title("Temporal Plot")

    elif space == 'spectral':
        plt.ylabel("Magnitude [dB]")
        if isNormalizedAxis:
            plt.xlim([0, 1])
            plt.xlabel("Normalized frequency [rad/sample]")
            plt.title("Spectral Plot, normalized frequencies")
        else:
            # if len(vect) == 1:
            #     plt.xlim(vect[0], vect[-1])
            # else:
            #     df = vect[-1] - vect[-2]
            #     plt.xlim(vect[0], vect[-1] + 10 * df)
            plt.xlabel("Frequency [Hz]")
            plt.title("Spectral Plot")

    else:
        logging.info("Impossible to label axis !")
        plt.xlim()
        plt.ylim()


def pshow(legend: list = None):
    """Plot Show
    Args:
        legend (list, optional): [legend list to plot]. Defaults to None.
    """
    plt.gcf()
    plt.grid()
    if legend is not None:
        plt.legend(legend)
    plt.show()


def boardControl(vect: list, data: list,
                 additionalData: list, legendList: list):
    """Displays nice plotting areas with fixed layout and informations about item

    Args:
        vect (list): [axis vector]
        data (list): [data vector]
        additionalData (list): [informations to display]
        legendList (list): [list of curves legends]
    """
    plt.figure()
    plt.title("Board Control")
    plt.subplot(1, 2, 1)
    shortPlot(vect[1], data[1], space="spectral", scale="semilog")
    plt.legend(legendList[1])
    plt.grid()
    plt.subplot(2, 2, 2)
    shortPlot(vect[0], data[0], space="time", scale="lin")
    plt.legend(legendList[0])
    plt.subplot(2, 2, 4)
    plt.text(x=0, y=0, s=additionalData.__str__())
    plt.show()
