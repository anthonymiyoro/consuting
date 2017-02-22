import time
import json
import requests
import urllib
from db import Database

TOKEN = '320053880:AAH-nr-2Je_tgUpaPm4GIyMnHk0iIloNzEU'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)
db = Database("/var/www/html/part3")


# collect url
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# parse url
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# collects messages sent to the bot every 100 seconds
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
# dont show any messages with smaller ids
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# collect last mesage sent to the bot
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


# sends the message contained in text to chat_id
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + \
        "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(
            text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


# return highest id of all recieved updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_update(update):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
# store all items from the database in the items variable
        items = db.get_items(chat)
# when they send /done, show keyboard menu
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select items to delete", chat, keyboard)
# if /start is sent, display message
        elif text == "/start":
            send_message(
                "Welcome to your Personal Automated To-Do List bot. Send any to do item and I'll store it. You can then send /done to remove items.", chat)
# if / is in the message then ignore
        elif text.startswith("/"):
            return
# bring back the menu after deleting an item
        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        else:
            # if not duplicate, add to db
            db.add_item(text, chat)
            items = db.get_items(chat)
            message = "\n".join(items)
            send_message(message, chat)




# loop through the updates then collect the text and chat
def handle_updates(updates):
    for update in updates["result"]:
        handle_update(update)


# create a keyboard with all the items, converts it to json
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


# infinite loop
# collect last sent text and echo it back, check every 0.5 seconds
def main():
    db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
