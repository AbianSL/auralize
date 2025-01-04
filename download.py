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
    """Descarga un archivo desde una URL y lo guarda localmente."""
    print(f"Descargando {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Archivo guardado en {save_path}")
        return False
    else:
        print(f"Error al descargar {url}. Código de estado: {response.status_code}")
        return True

def main():
    # Descargar metadatos
    print("Descargando metadatos...")
    download_file(METADATA_URL, METADATA_FILE)

    # Descargar archivos de audio
    print("Descargando archivos de audio...")
    
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
        print(f"{RED}Son 2000 archivos, esto puede tardar un rato.{RESET}")
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
    main()
