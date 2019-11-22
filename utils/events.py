import os

from colorama import Fore, init

from utils.evaluate_message import evaluate_message

init()


def logged_on():
    print(Fore.GREEN + '[+] Logged on successfully!')


def on_message(user, message):
    print(Fore.GREEN + f'[+] {user.steam_id}: {message}')

    os.chdir('./utils')

    file_name = 'logs.txt'

    try:
        file_size = os.path.getsize(file_name)
        if file_size > 25000:
            os.remove(file_name)
            print(Fore.RED + f'[-] Removed {file_name} because the file exceeded 5kb.')
        else:
            with open(file_name, 'a') as file:
                file.write(f'[+] {user.steam_id}: {message}\n')
    except FileNotFoundError:
        with open(file_name, 'a') as file:
            file.write(f'[+] Message received from {user.steam_id}: {message}\n')

    os.chdir('..')

    evaluate_message(user, message)
