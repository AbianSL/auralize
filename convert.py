import audio_file_names as afn
from audio.input import Audio

from pathlib import Path
import os
import sys

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

def convert_file(audio_path, save_path):
    """Convert an audio file to a spectrogram and save it."""
    audio = Audio(audio_path)
    audio.save_spectrogram(save_path)

def convert_all_files():
    """Convert all audio files to spectrograms."""
    
    verbose_flag = False
    reinstall_flag = False

    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "--small" or sys.argv[i] == "-s":
                afn.audio_names = afn.audio_names[:len(afn.audio_names) // 8]
            if sys.argv[i] == "--medium" or sys.argv[i] == "-m":
                afn.audio_names = afn.audio_names[:len(afn.audio_names) // 4]
            if sys.argv[i] == "--large" or sys.argv[i] == "-l":
                afn.audio_names = afn.audio_names[:len(afn.audio_names) // 2]
            if sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
                verbose_flag = True
            if sys.argv[i] == "--reinstall" or sys.argv[i] == "-r":
                reinstall_flag = True
            if sys.argv[i] == "--help" or sys.argv[i] == "-h":
                print("Uso: python setup.py [opciones]")
                print("Opciones:")
                print("  --small, -s    Descargar una octava parte de los archivos")
                print("  --medium, -m   Descargar un cuarto de los archivos")
                print("  --large, -l    Descargar la mitad de los archivos")
                print("  --verbose, -v  Mostrar mensajes detallados")
                print("  --reinstall, -r  Volver a descargar todos los archivos")
                print("  --help, -h     Mostrar este mensaje de ayuda")
                sys.exit()
    for audio_path in afn.audio_names:
        # -4 to remove the .wav extension
        save_path = SPEC_DIR / (audio_path[:-4] + ".png")
        convert_file(audio_path, save_path) 

if __name__ == "__main__":
    convert_all_files()
    print("Conversion complete.")
