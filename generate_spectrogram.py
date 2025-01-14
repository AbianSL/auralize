from pathlib import Path
from sys import argv
from audio.input import Audio

if __name__ == "__main__":
    if len(argv) != 2:
        exit(1)
    file_path = Path(argv[1])
    audio = Audio(file_path)
    audio.save_spectrogram(Path("spectrogram.png"));
