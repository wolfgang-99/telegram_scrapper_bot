import os, random
import logging
import subprocess
import sys

from manager import manager
from scraper import scraper
from tsadder import add_members
from security import main

main()

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))  # Directory of the executable
LOG_FILE = os.path.join(BASE_DIR, "log", "main.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('main.py')


def install_colorama():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("colorama is not installed. Installing colorama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])


def install_pyfiglet():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("Pyfiglet is not installed. Installing Pyfiglet...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])


try:
    from colorama import init, Fore
    import pyfiglet

except ImportError:
    install_colorama()
    install_pyfiglet()
    from colorama import init, Fore
    import pyfiglet


init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]


def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram')
    print(f'{random.choice(colors)}{banner}{n}')
    print(r + '  Version: 1.1 | Author: Wolfs_code' + n + '\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def main():

    clr()
    banner()
    print(lg + '[1] manage accounts' + n)
    print(lg + '[2] scrape source group' + n)
    print(lg + '[3] add member to target group' + n)
    print(lg + '[4] Quit')

    a = int(input(f'\nEnter your choice: {r}'))

    if a == 1:
        manager()
    if a == 2:
        scraper()
    if a == 3:
        add_members()
    if a == 4:
        clr()
        banner()
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        input("Press Enter to exit...")
