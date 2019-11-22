import json
import os

from colorama import Fore, init

from utils.email import Mail

init()

with open('config.json', 'r') as JSON:
    config = json.load(JSON)

def logged_on():
    print(Fore.GREEN + '[+] Logged on successfully!')


def on_message(user, message):
    print(Fore.GREEN + f'[+] {user.steam_id}: {message}')
    os.chdir('./utils')

    file_name = 'logs.txt'

    max_file_size = '5000'

    email = Mail(config['from_email'], config['from_email_password'], config['to_email'], 'Steam Messages Logs Report',
                 f'Report for the logs.txt file because it exceeds {int(max_file_size) / 1000}kb')

    try:
        file_size = os.path.getsize(file_name)
        if file_size > int(max_file_size):
            email.report_file(file_name)
            os.remove(file_name)
            print(Fore.RED + f'[-] Removed {file_name} because the file exceeded {int(max_file_size) / 1000}kb.')
        else:
            with open(file_name, 'a') as file:
                file.write(f'[+] Message received from {user.steam_id}: {message}\n\n')
    except FileNotFoundError:
        with open(file_name, 'a') as file:
            file.write(f'[+] Message received from {user.steam_id}: {message}\n\n')
    os.chdir('..')
