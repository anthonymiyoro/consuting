import time
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
    js = json.loads(content)
    return js


# collects messages sent to the bot
def get_updates():
    url = URL + "getUpdates"
# dont show any messages with smaller ids
    if offset:
        url += "?offset={}".format(offset)
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
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


# return highest id of all recieved updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# repeat every message sent to the bot
def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


# infinite loop
# collect last sent text and echo it back, check every 0.5 seconds
def main():
    last_textchat = (None, None)
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            send_message(text, chat)
            # saves last message id replied to
            last_textchat = (text, chat)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
