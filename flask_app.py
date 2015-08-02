
# A very simple Flask Hello World app for you to get started with...
import logging, sys
from flask import Flask, request
from CrapBot import Bot

crap_bot = Bot()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/bot', methods=['POST', 'GET'])
def bot():
    update = request.json
    if update:
        crap_bot.handle(update)
    return 'Ok'

if __name__ == '__main__':
    from CrapBot import Logger
    Logger.warn('bot started')
    #from CrapBot.Api import set_webhook
    #r = set_webhook()
    #print(r)
    crap_bot.listen()