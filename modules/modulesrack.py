import os
import sys

sys.path.append(os.getcwd())
from modules import audiofiltering_rt as rt_filtering

LAB_DEFAULT_CONFIG_DICT = {
    "MAX_INTEGER": 32768.0,
    "BUFFER_SIZE": 1024,
    "SAMPLING_RATE": 44100
}

class ModulesRack():
    """ Module rack gathering processing modules
    """
    def __init__(self):
        self.chunk = None
        self.module_items = []
        self.wiring = "waterfall"

    def load_and_process_chunk(self, chunk):
        if self.wiring == "waterfall":
            self.chunk = chunk
            self.process_by_parsing_items()

    def process_by_parsing_items(self):
        for module in self.module_items:
            self.chunk = module.process_and_return_chunk(self.chunk)

    def add_new_module(self, *new_module):
        self.module_items.append(*new_module)


class ModuleItem():
    """Module wrapper into module item format
    """
    def __init__(self, type: str = "Audio_filter_rt", subtype: str = "rt_bandpass"):
        self.input = None
        self.output = None
        self.module = None
        self.type = type
        self.subtype = subtype

        if self.type == "Audio_filter_rt":
            if self.subtype == "rt_bandpass":
                self.init_rt_bandpass()
        else:
            pass

    def process_and_return_chunk(self, chunk) -> list:
        self.input = chunk
        if self.type == "Audio_filter_rt":
            if self.subtype == "rt_bandpass":
                self.output = self.module.filter_buffer_data(self.input)
        else:
            self.output = self.input
        return self.output

    def init_rt_bandpass(self):
        self.module = rt_filtering.AudioFilter_rt(LAB_DEFAULT_CONFIG_DICT['SAMPLING_RATE'],
                                                  LAB_DEFAULT_CONFIG_DICT['BUFFER_SIZE'])
        self.module.set_bandpass(lowcut=150, highcut=2500, order=4)
        self.module.init_rt_filtering()