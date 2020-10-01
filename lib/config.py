import os, sys
from pathlib import Path

# general settings  
AUDIO_REPOSITORY = "D:/OneDrive/Documents/_PROJETS_PERSO/PROGRA/audio"
# audio general
SAMPLING_FREQUENCY = 44100  # Hz

# audiofile
AUDIO_SOURCES = Path(AUDIO_REPOSITORY, "sources")
AUDIO_FILE_TEST = Path(AUDIO_SOURCES, "joyca.wav")

# audiogenerator
BASIC_DURATION = 0.1  # sec