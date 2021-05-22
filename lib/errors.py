import os
import sys
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402


class InvalidRate(ValueError):
    pass


class InvalidFormat(ValueError):
    pass


class MissingVect(ValueError):
    pass
