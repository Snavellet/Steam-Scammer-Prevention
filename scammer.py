import gevent.monkey

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

from gevent import sleep
import steam.guard
import steam.client
import utils.events as event
from colorama import Fore, init
from steam.enums.common import EFriendRelationship
from utils.email import Mail, mail
from utils.check_scammer import check_scammer, check_scammer_name, check_scammer_name_message
import json
import re
import os

with open('config.json', 'r') as JSON:
    config = json.load(JSON)

init()

username = config['username']
password = config['password']
shared_secret = config['shared_secret']

guard = steam.guard.SteamAuthenticator(secrets={'shared_secret': shared_secret})
client = steam.client.SteamClient()

code = guard.get_code()

scammer_article = 'https://steamcommunity.com/sharedfiles/filedetails/?id=1261293152'  # The article for countering scammers

client.on('logged_on', callback=event.logged_on)


@client.friends.on("friend_invite")
def on_friend_request(user):
    reputation = check_scammer(user.steam_id)

    if reputation == 'SCAMMER':
        email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                     'Automatically Declined Friend Request',
                     mail(reputation, user.name, user.steam_id, scammer_article))
        print(Fore.RED + f'[-] Declining friend request from: {user.steam_id}')
        client.friends.remove(user)
        return email.report()

    greeting_message = config['greeting_message']

    if user.relationship == EFriendRelationship.RequestRecipient:
        email = Mail(config['from_email'], config['from_email_password'], config['to_email'], 'Accepted Friend Request',
                     mail(reputation, user.name, user.steam_id, scammer_article))

        search_link = re.findall(r'(htt\w+\W+)(\w+\.\w{3})', user.name)

        domains = []

        for el in search_link:
            domains.append(el[1])

        if len(domains) == 1:
            check_scammer_name(client, user,
                               f'Your name contains a domain: {", ".join(domains)}. These type of names will not be '
                               f'tolerated and '
                               f'therefore, I will remove you from my friendlist.')
        elif len(domains) > 1:
            check_scammer_name(client, user,
                               f'Your name contains multiple domains: {", ".join(domains)}. These type of names will '
                               f'not be '
                               f'tolerated and '
                               f'therefore, I will remove you from my friendlist.')
        else:
            if config['auto_accept'] == 'on':
                print(Fore.GREEN + f'[+] Accepting friend request from: {user.steam_id}')
                email.report()
                client.friends.add(user)
                sleep(2)
                user.send_message(greeting_message)
            elif config['auto_accept'] == 'off':
                email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                             'Declined Friend Request',
                             mail(reputation, user.name, user.steam_id, scammer_article))
                print(Fore.RED + f'[-] Declining friend request from: {user.steam_id}')
                client.friends.remove(user)
                email.report()
            else:
                email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                             'New Friend Request',
                             mail(reputation, user.name, user.steam_id, scammer_article))
                print(Fore.GREEN + f'[+] New friend request from: {user.steam_id}')
                email.report()


@client.on(client.EVENT_CHAT_MESSAGE)
def on_message(user, message):
    print(Fore.GREEN + f'[+] {user.steam_id}: {message}')

    reputation = check_scammer(user.steam_id)

    if reputation == 'SCAMMER':
        email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                     'Automatically Declined Friend Request',
                     mail(reputation, user.name, user.steam_id, scammer_article))
        print(Fore.RED + f'[-] Declining friend request from: {user.steam_id}')
        client.friends.remove(user)
        return email.report()

    search_link = re.findall(r'(htt\w+\W+)(\w+\.\w{3})', user.name)

    domains = []

    for el in search_link:
        domains.append(el[1])

    if len(domains) == 1:
        check_scammer_name_message(client, user,
                                   f'Your name contains a domain: {", ".join(domains)}. These type of names will not be '
                                   f'tolerated and '
                                   f'therefore, I will remove you from my friendlist.')
    elif len(domains) > 1:
        check_scammer_name_message(client, user,
                                   f'Your name contains multiple domains: {", ".join(domains)}. These type of names will '
                                   f'not be '
                                   f'tolerated and '
                                   f'therefore, I will remove you from my friendlist.')

    os.chdir('./utils')

    file_name = 'logs.txt'

    max_file_size = int(config['file_limit_report']) * 1000

    email = Mail(config['from_email'], config['from_email_password'], config['to_email'], 'Steam Messages Logs Report',
                 f'Report for the logs.txt file because it exceeds {max_file_size // 1000}kb')

    try:
        file_size = os.path.getsize(file_name)
        if file_size > int(max_file_size):
            email.report_file(file_name)
            os.remove(file_name)
            print(Fore.RED + f'[-] Removed {file_name} because the file exceeded {max_file_size // 1000}kb.')
        else:
            with open(file_name, 'a') as file:
                file.write(f'[+] Message received from {user.steam_id}: {message}\n\n')
    except FileNotFoundError:
        with open(file_name, 'a') as file:
            file.write(f'[+] Message received from {user.steam_id}: {message}\n\n')
    os.chdir('..')


client.login(username=username, password=password, two_factor_code=code)
client.run_forever()
