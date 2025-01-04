import audio_file_names as afn
from io. 
from pathlib import Path

# local paths
DOWNLOAD_DIR = Path("esc50_data")
AUDIO_DIR = DOWNLOAD_DIR / "spectrograms"
METADATA_FILE = DOWNLOAD_DIR / "esc50.csv"

# create directories if they don't exist
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

