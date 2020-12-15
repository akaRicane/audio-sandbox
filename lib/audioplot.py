import matplotlib.pyplot as plt

def shortPlot(vect, data, space='time', legendList: list=None):
    """Allows to plot multiple plots in one fig with some specific treatment

    Args:
        vect ([type]): [x axis]
        data ([type]): [y axis]
        space (str, optional): [time/spectral plot]. Defaults to 'time'.
    """
    plt.gcf()
    plt.ylabel("Amplitude")
    if not isinstance(data[0], list):
        if space == "time": 
            plt.plot(vect, data) if len(data) < len(vect) else plt.plot(vect[:len(data)], data)
            plt.xlabel("Time [s]")
        elif space == "spectral":
            plt.semilogx(vect, data) if len(data) < len(vect) else plt.semilogx(vect[:len(data)], data)
            plt.xlabel("Frequency [Hz]")
    else:
        for channel in range(len(data)):
            if space == "time":
                plt.plot(vect[:len(data[channel])], data[channel]) 
                plt.xlabel("Time [s]")
            elif space == "spectral":
                plt.semilogx(vect[:len(data[channel])], data[channel])
                plt.xlabel("Frequency [Hz]")
        

def pshow(legend: list=None):
    """Plot Show
    Args:
        legend (list, optional): [legend list to plot]. Defaults to None.
    """
    fig = plt.gcf()
    plt.grid()
    if legend is not None: plt.legend(legend)
    plt.show()


def boardControl(vect: list, data:list, additionalData: list, legendList: list):
    plt.figure()
    plt.title("Board Control")
    plt.subplot(1,2,1)
    shortPlot(vect[1], data[1], "spectral")
    plt.legend(legendList[1])
    plt.grid()
    plt.subplot(2, 2, 2)
    shortPlot(vect[0], data[0], "time")
    plt.legend(legendList[0])
    plt.subplot(2, 2, 4)
    plt.text(x=0, y=0, s=additionalData.__str__())
    plt.show()