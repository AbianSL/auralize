import audio_file_names as afn
from io.input import Audio 

from pathlib import Path
import os

# local paths
DOWNLOAD_DIR = Path("esc50_data")
AUDIO_DIR = DOWNLOAD_DIR / "audio"
METADATA_FILE = DOWNLOAD_DIR / "esc50.csv"
SPEC_DIR = DOWNLOAD_DIR / "spectrograms"

# detect if the audio directory exists
if not os.path.exists(AUDIO_DIR) or not os.path.isdir(AUDIO_DIR):
    print("The directory does not exist. Execute download.py first.")
    exit()

# create the spectrogram directory
SPEC_DIR.mkdir(parents=True, exist_ok=True)

