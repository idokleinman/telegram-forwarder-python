## change filename settings.template to settings.py and fill in all values

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
# from telethon.tl.functions.messages import ForwardMessagesRequest

import time
from settings import *

client = TelegramClient(username, api_id, api_hash)
client.connect()

# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    if not sign_in_code:
        print("Use >heroku config:set SIGN_IN_CODE=xxxxx [number you received from telegram notification] to restart dyno")
    try:
        # client.sign_in(phone, input('Enter the code: ')) # requires user typing - cannot run on heroku
        client.sign_in(phone, sign_in_code)
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: ')) # won't work

# me = client.get_me()
# print(me)

# group = client.get_entity('https://t.me/BtcollegeChat')
chnl = client.get_entity(from_channel_link)
target = client.get_entity(to_user)

# print(chnl)
# print(target)
print("-> Forwarding messages...")
last_msg_id = 0

while True:
    msgs = client.get_messages(chnl)
    new_msg = msgs[0]
    if new_msg.id != last_msg_id:
        last_msg_id = new_msg.id
        client.forward_messages(target, new_msg)
        print('New channel message forwarded:')
        print(new_msg.message)
    time.sleep(poll_interval)

# # If you only have the message IDs
# client.forward_messages(
#     entity,  # to which entity you are forwarding the messages
#     message_ids,  # the IDs of the messages (or message) to forward
#     from_entity  # who sent the messages?
# )
#
# # If you have ``Message`` objects
# client.forward_messages(
#     target,  # to which entity you are forwarding the messages
#     last_msg  # the messages (or message) to forward
# )
#
# # You can also do it manually if you prefer
#
#
# messages = foo()  # retrieve a few messages (or even one, in a list)
# from_entity = bar()
# to_entity = baz()
#
# client(ForwardMessagesRequest(
#     from_peer=from_entity,  # who sent these messages?
#     id=[msg.id for msg in messages],  # which are the messages?
#     to_peer=to_entity  # who are we forwarding them to?
# ))
