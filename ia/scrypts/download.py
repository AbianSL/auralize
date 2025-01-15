import requests
import sys
from time import sleep
from pathlib import Path

import audio_file_names as afn

# URLs base del repositorio ESC-50
BASE_URL = "https://raw.githubusercontent.com/karoldvl/ESC-50/master/"
AUDIO_DIR_URL = BASE_URL + "audio/"
METADATA_URL = BASE_URL + "meta/esc50.csv"

# ANSI escape codes for colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

# Unicode characters for tick and cross
tick = '\u2713'  # ✅
cross = '\u2717'  # ❎

# Rutas locales
DOWNLOAD_DIR = Path("esc50_data")
AUDIO_DIR = DOWNLOAD_DIR / "audio"
METADATA_FILE = DOWNLOAD_DIR / "esc50.csv"

# Crear directorios si no existen
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, save_path):
    """
        Download a file from a URL and save it to a local path
        Args:
            url: URL to download the file from
            save_path: Path to save the downloaded file
    """
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"file save in {save_path}")
        return False
    else:
        print(f"Error on downling {url}. state code: {response.status_code}")
        return True

def download_all_files():
    # Download metadata
    print("Downloading metadata...")
    download_file(METADATA_URL, METADATA_FILE)

    # Download audio files 
    print("Downloading audio files...")

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
                print("Usage: python download.py [OPTION]")
                print("Options:")
                print("  --small, -s\t\tDownload only 1/8 of the audio files")
                print("  --medium, -m\t\tDownload only 1/4 of the audio files")
                print("  --large, -l\t\tDownload only 1/2 of the audio files")
                print("  --verbose, -v\t\tShow progress bar")
                print("  --reinstall, -r\tReinstall all audio files")
                print("  --help, -h\t\tShow this help message")
                sys.exit() 
    if verbose_flag:
        from tqdm import tqdm
        for i in tqdm(range(len(afn.audio_names))):
            if not reinstall_flag and (AUDIO_DIR / afn.audio_names[i]).exists():
                print(f"{GREEN}{tick}{RESET}")
                continue
            filename = afn.audio_names[i]
            file_url = AUDIO_DIR_URL + filename
            save_path = AUDIO_DIR / filename
            if (download_file(file_url, save_path)):
                print(f"{RED}{cross}{RESET}")
            else:
                print(f"{GREEN}{tick}{RESET}")
            print()
    else:
        if len(afn.audio_names) > 500:
            print(f"{RED}Warning: {len(afn.audio_names)} files will be downloaded. This may take a while.{RESET}")
            sleep(2)

        for filename in afn.audio_names:
            if not reinstall_flag and (AUDIO_DIR / filename).exists():
                print(f"{GREEN}{tick}{RESET}")
                continue
            file_url = AUDIO_DIR_URL + filename
            save_path = AUDIO_DIR / filename
            if (download_file(file_url, save_path)):
                print(f"{RED}{cross}{RESET}")
            else:
                print(f"{GREEN}{tick}{RESET}")
            print()

    print("Descarga completa.")

if __name__ == "__main__":
    download_all_files()
