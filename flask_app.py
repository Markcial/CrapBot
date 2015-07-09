
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
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
        Commands.process(update)
    return 'Ok'

if __name__ == '__main__':
    processed_updates = []
    while True:
        updates = Api.getUpdates(offset=687926805)
        for update in updates['result']:
            update_id = update['update_id']
            if update_id not in processed_updates:
                processed_updates.append(update['update_id'])
                Commands.process(update)
        sleep(10)