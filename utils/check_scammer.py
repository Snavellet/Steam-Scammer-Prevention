import asyncio
import json

import aiohttp
from colorama import Fore
from gevent import sleep

from utils.email import Mail, mail

with open('config.json', 'r') as JSON:
    config = json.load(JSON)


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.json()


def check_scammer(steam_id):
    loop = asyncio.get_event_loop()
    check_banned = loop.run_until_complete(fetch(f'http://steamrep.com/api/beta4/reputation/{steam_id}?json=1'))

    reputation = check_banned['steamrep']['reputation']['summary']

    if reputation == 'none':
        reputation = 'SAFE'

    return reputation


scammer_article = 'https://steamcommunity.com/sharedfiles/filedetails/?id=1261293152'  # The article for countering scammers


def check_scammer_name(client, user, message):
    reputation = check_scammer(user.steam_id)

    email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                 'Automatically Declined Friend Request',
                 mail(reputation, user.name, user.steam_id, scammer_article))

    client.friends.add(user)
    sleep(2)
    user.send_message(message)
    sleep(3)
    client.friends.remove(user)
    email.report()
    print(Fore.RED + f'[-] Removed {user.steam_id} since name contains a domain.')


def check_scammer_name_message(client, user, message):
    reputation = check_scammer(user.steam_id)

    email = Mail(config['from_email'], config['from_email_password'], config['to_email'],
                 'Automatically Declined Friend Request',
                 mail(reputation, user.name, user.steam_id, scammer_article))
    user.send_message(message)
    sleep(3)
    client.friends.remove(user)
    email.report()
    print(Fore.RED + f'[-] Removed {user.steam_id} since name contains a domain.')
