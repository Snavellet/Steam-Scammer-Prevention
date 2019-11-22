import gevent.monkey

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

from gevent import sleep
import steam.guard
import steam.client
import utils.events as event
from colorama import Fore, init
import re
from steam.enums.common import EFriendRelationship

init()

username = ''
password = ''
shared_secret = ''

guard = steam.guard.SteamAuthenticator(secrets={'shared_secret': shared_secret})
client = steam.client.SteamClient()

code = guard.get_code()

client.on('logged_on', callback=event.logged_on)


@client.friends.on("friend_invite")
def on_friend_request(user):
    greeting_message = 'Hello, how can I assist you?'
    search_link = re.findall(r'(htt\w+\W+)(\w+\.\w{3})', user.name)

    if user.relationship == EFriendRelationship.RequestRecipient:
        domains = []

        for el in search_link:
            domains.append(el[1])

        def check_scammer_name(message):
            client.friends.add(user)
            sleep(2)
            user.send_message(message)
            sleep(3)
            client.friends.remove(user)
            print(Fore.RED + f'[-] Removed {user.steam_id} since name contains a domain.')

        if len(domains) == 1:
            check_scammer_name(f'Your name contains a domain: {", ".join(domains)}. These type of names will not be '
                               f'tolerated and '
                               f'therefore, I will remove you from my friendlist.')
        elif len(domains) > 1:
            check_scammer_name(f'Your name contains multiple domains: {", ".join(domains)}. These type of names will '
                               f'not be '
                               f'tolerated and '
                               f'therefore, I will remove you from my friendlist.')
        else:
            print(Fore.GREEN + f'[+] Accepting friend request from: {user.steam_id}')
            client.friends.add(user)
            sleep(2)
            user.send_message(greeting_message)


client.on(client.EVENT_CHAT_MESSAGE, callback=event.on_message)

client.login(username=username, password=password, two_factor_code=code)
client.run_forever()