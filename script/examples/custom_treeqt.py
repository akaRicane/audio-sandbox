import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

DEFAULT_TREE = [
    {'name': 'Parameters', 'type': 'group', 'children': [
        {'name': 'Integer', 'type': 'int', 'value': 10},
        {'name': 'Action Parameter', 'type': 'action'}
    ]}
]


class TreeParameters():

    def __init__(self, tree_architecture):

        self.app = QtGui.QApplication([])
        self.param = Parameter.create(name='Parameters', type='group', children=tree_architecture)
        # loop waiting modif in tree content
        self.param.sigTreeStateChanged.connect(self.change)
        self.param.sigValueChanging.connect(self.valueChanging)
        # create ParameterTree widget
        self.tree = ParameterTree()
        self.tree.setParameters(self.param, showTop=False)
        self.tree.setWindowTitle('pyqtgraph example: Parameter Tree')
        # generic call
        self.win = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
        self.layout.addWidget(self.tree)
        self.win.show()
        self.win.resize(800, 800)
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.param.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')

    def valueChanging(self, param, value):
        print("Value changing (not finalized): %s %s" % (param, value))


if __name__ == '__main__':
    from threading import Thread 
    gui = TreeParameters(DEFAULT_TREE)

    # thread = Thread(target=TreeParameters, args=DEFAULT_TREE)
    # thread.start() 
    # thread.join() 
    print("Thread Exiting...") 
