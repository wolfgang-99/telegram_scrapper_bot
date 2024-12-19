import sys
import logging
import os
import subprocess

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Python executable: {sys.executable}")
# logger.debug(f"Loaded modules: {list(sys.modules.keys())}")
logger.debug(f"Current working directory: {os.getcwd()}")


def install_telethon():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("Pyfiglet is not installed. Installing Pyfiglet...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "telethon"])

def install_colorama():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("colorama is not installed. Installing colorama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])


def install_pyfiglet():
    """Automatically installs PyInstaller if it is not already installed."""
    logger.info("Pyfiglet is not installed. Installing Pyfiglet...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])


try:
    from telethon.sync import TelegramClient
    from colorama import init, Fore
    import pyfiglet
    logger.info("imported all module successfully.")
except ImportError:
    logger.info("Not all module not found. Installing ...")
    install_telethon()
    install_colorama()
    install_pyfiglet()
    logger.error(" All module is successfully installed")


from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import time
import random
import pyfiglet
#import traceback
from colorama import init, Fore
import os



init()

r = Fore.RED
g = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, g, w, ye, cy]
info = g + '[' + w + 'i' + g + ']' + rs
attempt = g + '[' + w + '+' + g + ']' + rs
sleep = g + '[' + w + '*' + g + ']' + rs
error = g + '[' + r + '!' + g + ']' + rs


def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Telegram')
    print(random.choice(colors) + logo + rs)


def clscreen():
    os.system('cls')

clscreen()
banner()
api_id = int(sys.argv[1])
api_hash = str(sys.argv[2])
phone = str(sys.argv[3])
file = str(sys.argv[4])
group = str(sys.argv[5])
class Relog:
    def __init__(self, lst, filename):
        self.lst = lst
        self.filename = filename
    def start(self):
        with open(self.filename, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in self.lst:
                writer.writerow([user['username'], user['id'], user['access_hash'], user['group'], user['group_id']])
            f.close()
def update_list(lst, temp_lst):
    count = 0
    while count != len(temp_lst):
        del lst[0]
        count += 1
    return lst


users = []
with open(file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=',', lineterminator='\n')
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['user_id'] = row[1]
        user['access_hash'] = row[2]
        user['group'] = row[3]
        user['group_id'] = row[4]
        users.append(user)
client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
client.connect()
time.sleep(3)
target_group = client.get_entity(group)
entity = InputPeerChannel(target_group.id, target_group.access_hash)
group_name = target_group.title
print(f'{info}{g} Adding members to {group_name}{rs}\n')
n = 0
added_users = []
for user in users:
    n += 1
    added_users.append(user)
    if n % 50 == 0:
        print(f'{sleep}{g} Sleep 2 min to prevent possible account ban{rs}')
        time.sleep(120)
    try:
        if user['username'] == "":
            continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(entity, [user_to_add]))
        usr_id = user['user_id']
        print(f'{attempt}{g} Adding {usr_id}{rs}')
        print(f'{sleep}{g} Sleep 2 mins {rs}')
        time.sleep(120)
    except PeerFloodError:
        #time.sleep()
        os.system(f'del {file}')
        sys.exit(f'\n{error}{r} Aborted. Peer Flood Error{rs}')
    except UserPrivacyRestrictedError:
        print(f'{error}{r} User Privacy Restriction{rs}')
        continue
    except KeyboardInterrupt:
        print(f'{error}{r} Aborted. Keyboard Interrupt{rs}')
        update_list(users, added_users)
        if not len(users) == 0:
            print(f'{info}{g} Remaining users logged to {file}')
            logger = Relog(users, file)
            logger.start()
    except:
        print(f'{error}{r} Some Other error in adding{rs}')
        continue
#os.system(f'del {file}')
input(f'{info}{g}Adding complete...Press enter to exit...')
sys.exit()
