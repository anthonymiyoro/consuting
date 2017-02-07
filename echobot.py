import json
import requests

TOKEN = '320053880:AAH-nr-2Je_tgUpaPm4GIyMnHk0iIloNzEU'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

# collect url
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# parse url
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(contnet)
    return js

# collects messages sent to the bot
def get_updates():
	url = URL + "getUpdates"
	js = get_json_from_url(url)
	return js

# collect last mesage sent to the bot
def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return (text, chat_id)

def send_message(text, chat_id):
	url = URL + "sendMessage?"