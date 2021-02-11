import matplotlib.pyplot as plt
import logging


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
            df = vect[-1] - vect[-2]
            plt.xlim(vect[0], vect[-1] + 10 * df)
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
    return fig


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
