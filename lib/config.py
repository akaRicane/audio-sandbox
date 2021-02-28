import os
import pyaudio
from pathlib import Path

# general settings
AUDIO_REPOSITORY = os.getcwd()  # GIT root of repo

# audio general
SAMPLING_FREQUENCY = 44100  # Hz
FFT_SIZE = 1024  # points
BANDS_SLICER_SIZE = 10  # bands
FRAMES_PER_BUFFER = 1024  # frames per buffer
BYTES_DEFAULT_FORMAT = pyaudio.paInt16

# audiofile
AUDIO_RESSOURCES = Path(AUDIO_REPOSITORY, "resources")
AUDIO_FILE_JOYCA = Path(AUDIO_RESSOURCES, "joyca.wav")
AUDIO_FILE_TEST = Path(AUDIO_RESSOURCES, "gaussian_white_noise.wav")
AUDIO_FILE_SWEEP = Path(AUDIO_RESSOURCES, "CSC_sweep_20-20k.wav")

# audiogenerator
BASIC_DURATION = 0.1  # sec

# audiofiltering
BANDPASS_DEFAULT_ORDER = 5

# musical keys dict ref
REF_KEYS_DICT = {
    "Unit": "Hz",
    "A0": 27.50000,
    "A#0": 29.13524,
    "B0": 30.86771,
    "C1": 32.70320,
    "C#1": 36.70810,
    "D1": 36.70810,
    "D#1": 38.89087,
    "E1": 41.20344,
    "F1": 43.65353,
    "F#1": 46.24930,
    "G1": 48.99943,
    "G#1": 51.91309,
    "A1": 55.00000,
    "A#1": 58.27047,
    "B1": 61.73541
}
