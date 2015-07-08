
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from CrapBot import Commands, Api
from time import sleep

app = Flask(__name__)

api = Api()

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/bot', methods=['POST', 'GET'])
def bot():
    update = request.json
    if update:
        chat_id = update['message']['chat']['id']
        cmd = update['message']['text']
        message = Commands.match(cmd)
        api.sendMessage({'chat_id': chat_id, 'text':message})
    return 'Ok'

if __name__ == '__main__':
    processed_updates = []
    while True:
        updates = api.getUpdates()
        for update in updates['result']:
            update_id = update['update_id']
            if update_id not in processed_updates:
                processed_updates.append(update['update_id'])
                cmd = update['message']['text']
                chat_id = update['message']['chat']['id']
                message = Commands.match(cmd)
                api.sendMessage({'chat_id': chat_id, 'text': message})
        sleep(10)