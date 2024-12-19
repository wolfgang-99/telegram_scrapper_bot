import sqlite3
import os

print(os.path.join(sqlite3.__file__))




# Use sys.executable for the Python interpreter path
if hasattr(sys, '_MEIPASS'):
    # Running in PyInstaller bundle
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

usradder_path = os.path.join(BASE_DIR, "usradder.py")

# Safely construct the command
try:
    print(f"Using Python interpreter: {sys.executable}")
    print(f"Path to usradder.py: {usradder_path}")

    subprocess.Popen(
        ["cmd", "/k", sys.executable, usradder_path, str(api_id), str(api_hash), str(phone), file, group,
         scraped_grp])
    print(f"{plus}{lg} Launched from {phone}")
except Exception as e:
    print(f"{error}{r} Failed to launch: {e}")