def evaluate_message(user, message):
    prefix = '!'

    if not message.startswith(prefix):
        return

    if message == f'{prefix}blocked':
        user.send_message()
