from random import choice
from CrapBot.Api import send_message, send_photo, send_document, get_me
from CrapBot.Api.Objects import ForceReply


class Command(object):
    def __init__(self, bot):
        self.bot = bot


class SteppedCommand(Command):
    def __init__(self, bot):
        super(SteppedCommand, self).__init__(bot)
        self.current = 1

    def next(self, update):
        stp = 'step{0:d}'.format(self.current)
        if not hasattr(self, stp):
            return
        func = getattr(self, stp)
        func(update)
        self.current += 1

    def done(self):
        self.bot.conversation = None
        self.bot.current_command = None

class Status(Command):
    def main(self, update):
        status = get_me()
        send_message(update.message.chat.identifier, 'status {}'.format(status['result']))


class Salute(Command):
    def __init__(self, bot):
        super(Salute, self).__init__(bot)

    def main(self, update):
        whom = " ".join(update.message.text.split(" ")[1:])
        if whom == '':
            whom = 'tú!'
        send_message(update.message.chat.identifier, 'hola {}'.format(whom))


class SaveQuote(SteppedCommand):
    def main(self, update):
        response = send_message(
            update.message.chat.identifier,
            'Que frase quieres guardar?',
            reply_to_message_id=update.message.identifier,
            reply_markup=ForceReply(False)
        )
        self.message_id = response['result']['message_id']
        self.bot.conversation = True
        self.bot.current_command = self

    def step1(self, update):
        if not hasattr(update.message, 'reply_to_message') or update.message.reply_to_message.identifier != self.message_id:
            print('not the message i was expecting')
            return
        quotes = []
        if self.bot.storage.exists('quotes'):
            quotes = self.bot.storage.get('quotes')
        quotes.append(update.message.text)
        self.bot.storage.save('quotes', quotes)
        send_message(
            update.message.chat.identifier,
            'Almacenada!'
        )
        self.done()

class RandomQuote(Command):
    def main(self, update):
        quotes = []
        if self.bot.storage.exists('quotes'):
            quotes = self.bot.storage.get('quotes')
        send_message(update.message.chat.identifier, choice(quotes))


class SaveImage(SteppedCommand):
    def main(self, update):
        send_message(
            update.message.chat.identifier,
            'Que imagen quieres guardar?',
            reply_to_message_id=update.message.identifier,
            reply_markup=ForceReply()
        )
        self.bot.conversation = True
        self.bot.current_command = self

    def step1(self, update):
        files = []
        if self.bot.storage.exists('files'):
            files = self.bot.storage.get('files')
        data = dict()
        m = update.message
        print('type', m.type)
        if m.type == 'document':
            data['type'] = m.type
            data['file_id'] = m.document.identifier
            files.append(data)
        elif m.type == 'photo':
            for p in m.photo:
                print(p)
                data['type'] = m.type
                data['file_id'] = p.identifier
                files.append(data)
        self.bot.storage.save('files', files)
        send_message(
            update.message.chat.identifier,
            'Almacenada!'
        )
        self.done()

class RandomImage(Command):
    def main(self, update):
        files = []
        if self.bot.storage.exists('files'):
            files = self.bot.storage.get('files')
        fl = choice(files)
        if fl['type'] == 'document':
            send_document(update.message.chat.identifier, fl['file_id'])
        elif fl['type'] == 'photo':
            send_photo(update.message.chat.identifier, fl['file_id'])