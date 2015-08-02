import logging
import pickle
import os
from time import sleep
from CrapBot import Config
from CrapBot.Api.Objects import Update
from CrapBot.Api import send_message, send_photo, send_sticker, get_updates
from CrapBot.Commands import Salute, Status, SaveQuote, RandomQuote, SaveImage, RandomImage

stickers = {
    'lol': 'BQADBAADPgEAAvCZ8AABEmXm6q67HeYC',
    'mother of god': 'BQADBAADQgEAAvCZ8AABgPc1a9E8alkC',
    'okay': 'BQADBAADRgEAAvCZ8AABHoOEPhSB4pQC',
    '¬¬': 'BQADBAADUAEAAvCZ8AABtsKuOknJmtUC',
    'why yu no': 'BQADBAADXAEAAvCZ8AABJLmZNP77M3YC',
    'so cute': 'BQADBAADYAEAAvCZ8AABGB6AWt6smKUC',
    'fuck': 'BQADBAADNAEAAvCZ8AABBdvOgHaaJDwC',
    'zaska': 'BQADBAADCQEAAvlsRwIMgoylEAX5rAI',
    'like a sir': 'BQADBAAD2wEAAvlsRwIOLYS2mMtnCwI'
}

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class Storage(object):
    def __init__(self):
        self.db = Bunch()
        if os.path.exists(Config.cache_file):
            self.db = pickle.load(open(Config.cache_file, 'rb'))

    def save(self, name, val):
        setattr(self.db, name, val)
        pickle.dump(self.db, open(Config.cache_file, 'wb'))

    def exists(self, name):
        return hasattr(self.db, name)

    def get(self, name):
        return getattr(self.db, name)


class Bot(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.listening = False
        self.conversation = None
        self.offset = None
        self.storage = Storage()
        self.commands = {}
        self.current_command = None
        self.add_command('status', Status)
        self.add_command('salute', Salute)
        self.add_command('save_quote', SaveQuote)
        self.add_command('random_quote', RandomQuote)
        self.add_command('save_image', SaveImage)
        self.add_command('random_image', RandomImage)

    def add_command(self, name, cmd):
        self.commands[name] = cmd(self)

    def listen(self):
        logging.debug('ffffff')
        self.listening = True
        while self.listening:
            response = get_updates(offset=self.offset)
            for u in response['result']:
                self.handle(Update(u['update_id'], u['message']))
                self.offset = u['update_id'] + 1
            sleep(5)

    def handle(self, update):

        print(update)

        # do we have a conversation already started?
        if self.conversation is not None:
            # normal flow for the conversation until it cancels the conversation
            print('conversation!')
            self.current_command.next(update)

        if update.message.type == 'text':
            if update.message.text[0] == '/':
                command = update.message.text[1:].split(" ")[0].lower()
                if command in self.commands.keys():
                    cmd = self.commands[command]
                    cmd.main(update)

