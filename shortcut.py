import subprocess
import os
import sys
import logging
import traceback
import winshell


BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))  # Directory of the executable/script
LOG_FILE = os.path.join(BASE_DIR, "log", "shortcut.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('shortcut.py')

def create_shortcut(exe_path, shortcut_name, shortcut_dir=None):
    """
    Create a shortcut for the given executable.

    :param exe_path: Path to the .exe file
    :param shortcut_name: Desired name of the shortcut
    :param shortcut_dir: Directory where the shortcut will be created (defaults to Desktop)
    """
    # Default to the desktop directory
    shortcut_dir = shortcut_dir or winshell.desktop()
    shortcut_path = os.path.join(shortcut_dir, f"{shortcut_name}.lnk")

    # Get the parent directory of the .exe
    exe_dir = os.path.dirname(exe_path)

    # Create the shortcut
    with winshell.shortcut(shortcut_path) as shortcut:
        shortcut.path = exe_path
        shortcut.description = f"Shortcut to {shortcut_name}"
        shortcut.icon_location = (exe_path, 0) # Set icon location
        shortcut.working_directory = exe_dir  # Set working directory to .exe's parent folder

    print(f"Shortcut created at: {shortcut_path}")
    logger.info(f"Shortcut created at: {shortcut_path}")
    input("Press Enter to exit...")


try:
    # Dynamically determine the path to `Tele-scrapper.exe`
    exe_name = "Tele-scrapper.exe"
    exe_path = os.path.join(BASE_DIR, exe_name)

    # Check if the executable exists
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"The executable '{exe_name}' was not found in '{BASE_DIR}'.")

    # Create the shortcut
    create_shortcut(
        exe_path=exe_path,  # Dynamic path to the .exe file
        shortcut_name="Telegram Scrapper"  # Desired shortcut name
    )
except Exception as e:
    # Log and display the error
    logger.error(f"An error occurred: {e}")
    traceback.print_exc()  # Display full traceback for debugging
    input("An error occurred. Press Enter to exit...")  # Pause for user input
