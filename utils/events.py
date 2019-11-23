import json

from colorama import Fore, init
from steam.client import SteamClient

init()

client = SteamClient()

with open('config.json', 'r') as JSON:
    config = json.load(JSON)


def logged_on():
    print(Fore.GREEN + '[+] Logged on successfully!')

