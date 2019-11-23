import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail():
    def __init__(self, from_email, password, to_email, subject, message):
        self.from_email = from_email
        self.password = password
        self.to_email = to_email
        self.subject = subject
        self.message = message

    def report(self):
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        msg = MIMEMultipart()

        msg['Subject'] = self.subject
        msg['From'] = self.from_email
        msg['To'] = self.to_email

        msg.attach(MIMEText(self.message, 'plain'))
        text = msg.as_string()

        server.starttls()
        server.login(self.from_email, self.password)
        server.sendmail(self.from_email, self.to_email, text)
        server.quit()

    def report_file(self, file_name):
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.from_email
        msg['To'] = self.to_email

        msg.attach(MIMEText(self.message, 'plain'))
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("logs.txt", "rb").read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f'attachment; filename="{file_name}"')

        msg.attach(part)

        text = msg.as_string()

        server.starttls()
        server.login(self.from_email, self.password)
        server.sendmail(self.from_email, self.to_email, text)
        server.quit()


def mail(reputation, name, steam_id, article):
    return f'''[+] Reputation: {reputation}\n[+] Name: {name}\n[+] Steam Profile: https://steamcommunity.com/profiles/{steam_id}\n[+] SteamREP: https://steamrep.com/search?q={steam_id}\n\n[++] Important: {article}'''
