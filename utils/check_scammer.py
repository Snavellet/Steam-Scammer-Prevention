import asyncio

import aiohttp
from colorama import Fore
from gevent import sleep


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


def check_scammer_name(client, user, message):
    client.friends.add(user)
    sleep(2)
    user.send_message(message)
    sleep(3)
    client.friends.remove(user)
    print(Fore.RED + f'[-] Removed {user.steam_id} since name contains a domain.')


def check_scammer_name_message(client, user, message):
    user.send_message(message)
    sleep(3)
    client.friends.remove(user)
    print(Fore.RED + f'[-] Removed {user.steam_id} since name contains a domain.')
