import matplotlib.pyplot as plt
from lib import audiogenerator

def shortPlot(vect, data, space='time'):
    """Allows to plot multiple plots in one fig with some specific treatment

    Args:
        vect ([type]): [x axis]
        data ([type]): [y axis]
        space (str, optional): [time/spectral plot]. Defaults to 'time'.
    """
    plt.gcf()
    if space == "time": plt.plot(vect, data) 
    elif space == "spectral": plt.semilogx(vect, data[:len(vect)])
        

def pshow(legend: list=None):
    """Plot Show
    Args:
        legend (list, optional): [legend list to plot]. Defaults to None.
    """
    fig = plt.gcf()
    plt.grid()
    if legend is not None: plt.legend(legend)
    plt.show()
