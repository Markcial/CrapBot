
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import os
from CrapBot import Commands, Api
from time import sleep

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/bot', methods=['POST', 'GET'])
def bot():
    update = request.json
    if update:
        cmd = update['message']['text']
        Commands.match(cmd)
        return 'Ok'
    Commands.match('/help')
    return 'Ok!'

if __name__ == '__main__':
    api = Api()
    updates = api.getUpdates()
    print(updates)
    print([m['message']['text'] for m in updates['result']])
    print(Commands.match('/asdsa mensaje miguelin'))
    print(api.sendMessage({'chat_id':12122426,'text':"Hola Mundo!"}))