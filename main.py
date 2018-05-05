from bottle import request, route, run, template
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import time
from settings import *
from multiprocessing import Process

count_msgs = 0
last_msg_text = ''
proc = 0
session = 'inactive'

def start_forwarding(client):
	print("-> Starting forwarder...")
	chnl = client.get_entity(from_channel_link)
	target = client.get_entity(to_user)
	last_msg_id = 0

	print("-> Forwarding messages...")
	session = 'active'
	while True:
		msgs = client.get_messages(chnl)
		new_msg = msgs[0]
		if new_msg.id != last_msg_id:
			last_msg_id = new_msg.id
			client.forward_messages(target, new_msg)
			print('New channel message forwarded:')
			print(new_msg.message)
			last_msg_text = new_msg.message
			count_msgs += 1
		time.sleep(poll_interval)


def spawn_forwarding_process(client):
	global proc
	if __name__ == '__main__':
		if proc == 0 or not proc.is_alive():
			print("-> spawning forwarding process...")
			proc = Process(target=start_forwarding, args=(client,))
			proc.daemon = True
			proc.start()
		else:
			print("-> forwarding process already running.")


def start_server(client):
	print("-> Starting server...")
	@route('/')
	def login():
		print("-> Serving /")
		if not client.is_user_authorized():
			try:
				client.send_code_request(phone)
				return '''
					<h2>Telegram sign in</h2>
					<form action="/" method="post">
						Sign in code: <input name="sign_in_code" type="text" />
						<input value="Submit" type="submit" />
					</form>
				'''
			except:
				return '''
					<h2>Telegram sign in</h2>
					<p>Error while trying to login. (Most probably FloodError - wait 24 hours)...</p>
				'''
		else:
			spawn_forwarding_process(client)
			return template('<h2>Telegram session {{session_status}}</h2><p>Messages forwarded: {{count}}</p><p>Last message: {{msg}}</p>', count=count_msgs, msg=last_msg_text, session_status=session)

	@route('/', method='POST')
	def do_login():
		print("-> Got POST form")
		# try to login using the code from the user
		sign_in_code = request.forms.get('sign_in_code')
		client.sign_in(phone, sign_in_code)
		if client.is_user_authorized():
			spawn_forwarding_process(client)
			return "<p>Signed in successfully.</p>"
		else:
			return "<p>Incorrect code - please retry.</p>"

	# run(host='localhost', port=8080)
	run(host='0.0.0.0', port=int(os.getenv("PORT")))



def start():
	print("-> trying Telegram login...")
	client = TelegramClient(username, api_id, api_hash)
	client.connect()
	start_server(client)

start()
