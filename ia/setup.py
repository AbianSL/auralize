import sys
from pathlib import Path
import subprocess

# Paths to the modules
DOWNLOAD_SCRIPT = Path("scrypts/download.py")
CONVERT_SCRIPT = Path("scrypts/convert.py")

# Help text
HELP_TEXT = """
Usage: python setup.py [options]
Options:
  --small, -s        Download and convert 1/8 of the files
  --medium, -m       Download and convert 1/4 of the files
  --large, -l        Download and convert 1/2 of the files
  --all, -a          Download and convert all files
  --verbose, -v      Show detailed messages
  --reinstall, -r    Redownload and reconvert files
  --help, -h         Show this help message
"""

def execute_script(script_path, args):
    """
    Executes a Python script with the provided arguments.
    """
    command = [sys.executable, str(script_path)] + args
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
        sys.exit(1)

def main():
    """
    Process arguments and execute the corresponding actions.
    """
    if "--help" in sys.argv or "-h" in sys.argv:
        print(HELP_TEXT)
        sys.exit(0)

    # Determine arguments for the scripts
    download_args = []
    convert_args = []

    for arg in sys.argv[1:]:
        if arg in {"--small", "-s", "--medium", "-m", "--large", "-l", "--verbose", "-v", "--reinstall", "-r"}:
            download_args.append(arg)
            convert_args.append(arg)
        else:
            print(f"Unknown argument: {arg}")
            print(HELP_TEXT)
            sys.exit(1)

    # Execute download
    print("Starting download...")
    execute_script(DOWNLOAD_SCRIPT, download_args)

    # Execute conversion
    print("Starting conversion...")
    execute_script(CONVERT_SCRIPT, convert_args)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
