import copy

from lib import audiodata

class AudioItem():
    def __init__(self):
        # Common parameters of AudioItem
        self.nchannel = 0
        self.codec = None
        self.data = []
    
    # Channel Management
    def addChannel(self):
        self.data.append(audiodata.AudioData())
        self.nchannel = len(self.data)

    def deleteChannel(self, indexToDelete):
        del self.data[indexToDelete]
        self.nchannel = len(self.data)
        
    def cloneChannel(self, indexToClone):
        self.addChannel()
        self.data[-1] = copy.deepcopy(self.data[indexToClone])

    def makeStereo(self):
        self.cloneChannel(indexToClone=0)

    def setAudioItemToMono(self, indexToKeep=0):
        self.data[0] = copy.deepcopy(self.data[indexToKeep])
        for idx, _ in enumerate(self.data):
            if idx != 0:
                self.deleteChannel(idx)
        del idx, _
    
    def addSinusAsNewChannel(self):
        self.addChannel()
        self.data[-1] = slicer.loadSinus()
