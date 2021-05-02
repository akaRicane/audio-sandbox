import os
import sys
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402

INVALID_RATE = "Invalid given rate.\n"\
               f"Must be in {config.VALID_SAMPLERATES}"
