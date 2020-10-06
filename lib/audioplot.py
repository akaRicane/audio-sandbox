import matplotlib.pyplot as plt
from lib import audiogenerator

def shortPlot(vect, data, space='time'):
    fig = plt.gcf()
    legend = []
    if space == "time":
        plt.plot(vect, data)
    if space == "spectral":
        if len(data) == 2:
            plt.semilogx(vect, data[0], vect, data[1])
            legend.append('Channel 1')
            legend.append('Channel 2')
        elif len(data) == len(vect):
            plt.semilogx(vect, data)
            legend.append('Audio Data [Mono]')
    # TODO add automatic labelling
    plt.legend(legend)

def pshow():
    fig = plt.gcf()
    plt.show()
