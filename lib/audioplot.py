import matplotlib.pyplot as plt
from lib import audiogenerator

def shortPlot(vect, data, space='time'):
    fig = plt.gcf()
    if space == "time":
        plt.plot(vect, data)
    if space == "spectral":
        plt.semilogx(vect, data)
    # TODO add automatic labelling

def pshow():
    fig = plt.gcf()
    plt.show()
