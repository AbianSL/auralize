
from pathlib import Path
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from audio.input import Audio
import audio_file_names as afn
# local paths
DOWNLOAD_DIR = Path("esc50_data")
AUDIO_DIR = DOWNLOAD_DIR / "audio"
METADATA_FILE = DOWNLOAD_DIR / "esc50.csv"
SPEC_DIR = DOWNLOAD_DIR / "spectrograms"

# ANSI escape codes for colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

# Unicode characters for tick and cross
tick = '\u2713'  # ✅
cross = '\u2717'  # ❎

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

def change_metadata(metadata_path):
    """ Change the metadata file from .wav to .png
        Args:
            metadata_path: Path to the metadata file
    """
    try:
        with open(metadata_path, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace(".wav", ".png")
        with open(metadata_path, "w") as f:
            f.writelines(lines)
    except Exception as e:
        print(f"Error changing metadata: {e}")
        print(f"{RED}{cross}{RESET}")
        exit()

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

    if verbose_flag:
        print("Converting audio files to spectrograms...")
        from tqdm import tqdm
        for audio_file in tqdm(afn.audio_names):
            # -4 to remove the .wav extension
            save_path = SPEC_DIR / (audio_file[:-4] + ".png")
            audio_path = AUDIO_DIR / audio_file
            if save_path.exists():
                continue
            if audio_path.exists():
                if not reinstall_flag and save_path.exists():
                    continue
            try:
                convert_file(audio_path, save_path)
            except Exception as e:
                print(f"Error converting {audio_file}: {e}")
                continue
    else:
        for audio_file in afn.audio_names:
            # -4 to remove the .wav extension
            save_path = SPEC_DIR / (audio_file[:-4] + ".png")
            audio_path = AUDIO_DIR / audio_file
            if save_path.exists():
                print(f"{GREEN}{tick}{RESET}")
                continue
            if audio_path.exists():
                if not reinstall_flag and save_path.exists():
                    print(f"{GREEN}{tick}{RESET}")
                    continue
            try:
                convert_file(audio_path, save_path)
                print(f"{GREEN}{tick}{RESET}") 
            except Exception as e:
                print(f"{RED}{cross}{RESET}")
                print(f"Error converting {audio_file}: {e}")
                continue

if __name__ == "__main__":
    print("Converting audio files to spectrograms...")
    convert_all_files()
    print(f"{GREEN}{tick}{RESET}")
    print("Changing metadata file...")
    change_metadata(METADATA_FILE)
    print(f"{GREEN}{tick}{RESET}")
