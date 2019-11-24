# Steam Scammer Prevention
A bot made in Python to prevent scammers from scamming you.

# Features

* Automatically decline friend requests if the username contains a domain
* Check messages for dangerous links
* Send reports for friend requests
* Send logs of messages whenever the file limit is reached
* Automatically decline friend requests if the user is marked in [SteamREP](https://steamrep.com/)

# Setup
* pip install -r requirements.txt - Install all packages
* Input your details in config.json
* Run scammer.py

# Requirement
**[Python](https://www.python.org/)** --> 3.6 or more 

# Configuration

```json
{
  "username": "THE STEAM USERNAME FOR THE BOT", 
  "password": "THE STEAM PASSWORD FOR THE BOT",
  "shared_secret": "YOUR SHARED SECRET FOR GETTING THE 2FA CODE --> https://www.youtube.com/watch?v=JjdOJVSZ9Mo",
  "from_email": "YOUR EMAIL USED FOR SENDING REPORTS - FOR GMAIL, BE SURE LESS SECURE APP IS ENABLED --> https://devanswers.co/allow-less-secure-apps-access-gmail-account/",
  "from_email_password": "YOUR EMAIL USED FOR SENDING REPORTS - PASSWORD",
  "to_email": "THE EMAIL TO RECEIVE THE PASSWORD",
  "auto_accept": "ON - AUTOMATICALLY ACCEPT AND SEND YOU A REPORT || OFF - AUTOMATICALLY DECLINE AND SEND YOU REPORT || LEAVE IT EMPTY IF YOU DONT WANT TO ACCEPT OR DECLINE",
  "greeting_message": "GREETING MESSAGE FOR GREETING PEOPLE AFTER ACCEPTING THE FRIEND REQUEST - ONLY WORKS IF AUTO ACCEPT IS ON",
  "file_limit_report": "LOGS FILE FOR MESSAGES, LIMIT IN KB TO REPORT WHENEVER IT REACHES THAT LIMIT OR MORE"
}
```

# Made By
**Snavellet** --> Primary Developer

# License
MIT