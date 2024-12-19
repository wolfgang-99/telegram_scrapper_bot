import subprocess
import os
import sys
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../log/builder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('builder.py')


def install_pyinstaller():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("PyInstaller is not installed. Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def check_python_installed():
    """Check if Python is installed by trying to run the 'python --version' command."""
    try:
        logger.info("Checking if Python is installed...")
        subprocess.check_call(["python", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(" Python is installed...")
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def install_python():
    """Installs Python silently using a pre-downloaded installer."""
    installer_path = "python-3.10.7-amd64.exe"  # Make sure the installer is in the project folder
    logger.info("Python is not installed. Installing Python...")

    # Run the Python installer silently
    subprocess.check_call([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], shell=True)

    logger.info("Python installed successfully. Please restart your terminal and run the script again.")
    sys.exit(1)  # After installation, exit to allow Python to be added to the system PATH


def build_executable():
    """Builds the executable from the specified Python script."""
    script_to_compile = os.path.abspath("../main.py")
    output_folder = os.path.abspath("builder-EXE")  # Output folder for the executable
    icon_path = os.path.abspath("wolf_code.ico")  # Path to the .ico file

    # Check if Python is installed
    if not check_python_installed():
        install_python()

        # Try importing PyInstaller to check if it's installed
    try:
        import PyInstaller
    except ImportError:
        install_pyinstaller()

    # Remove the output directory if it exists (to avoid accumulating old files)
    if os.path.exists(output_folder):
        logger.info(f"Cleaning up the existing '{output_folder}' directory...")
        shutil.rmtree(output_folder)

    # Recreate the output directory
    os.makedirs(output_folder)

    # Use PyInstaller to compile the script
    try:
        pyinstaller_path = os.path.join(sys.exec_prefix, 'Scripts', 'pyinstaller.exe')
        logger.info(f"Building executable from {script_to_compile} into {output_folder}")

        # Compile with PyInstaller and direct all output to the 'builder-EXE' folder
        subprocess.check_call([
            pyinstaller_path,
            "--onefile",
            "--distpath", output_folder,  # Where the executable will be saved
            "--workpath", os.path.join(output_folder, "build"),  # Where the build folder will be saved
            "--specpath", output_folder,  # Where the .spec file will be saved
            "--icon", icon_path,  # Set the icon for the executable
            # "--hidden-import", "winshell",
            # "--hidden-import", "win32com",
            # "--hidden-import", "win32con",
            # "--hidden-import", "win32api",
            "--hidden-import", "telethon",
            "--hidden-import", "telethon.sync",
            "--hidden-import", "telethon.tl",
            "--hidden-import", "telethon.tl.types",
            "--hidden-import", "telethon.tl.functions",
            "--hidden-import", "pyfiglet",  # Include the pyfiglet module
            "--hidden-import", "pyfiglet.fonts",  # Include the pyfiglet.fonts submodule
            "--collect-data", "pyfiglet",
            # "--hidden-import", "_sqlite3",
            # "--collect-data", "_sqlite3",
            # "--add-data", "../../usradder.py;.",
            "--name", 'Tele-scrapper',
            # "--add-binary=C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python310\\DLLs\\sqlite3.dll:sqlite3",
            # "--add-binary=C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python310\\lib\\sqlite3\\__init__.py:sqlite3",

            script_to_compile
        ])

        logger.info(f"Build completed. Check the '{output_folder}' folder for the new executable.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Error during the build process: {e}")


if __name__ == "__main__":
    build_executable()
