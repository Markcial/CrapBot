
import re
from random import choice
from CrapBot.Api import sendMessage, sendPhoto, sendSticker

def matches(pattern):
    def decorator(fn):
        def match(subject):
            expr = re.compile(pattern)
            matches = expr.match(subject)
            if matches:
                return matches.groupdict()
            return False
        fn.match = match
        return fn
    return decorator

quotes = [
    "Hey everybody! Check out my package!",
    "Let's get this party started!",
    "Glitching weirdness is a term of endearment, right?",
    "Recompiling my combat code!",
    "This time it'll be awesome, I promise!",
    "Look out everybody! Things are about to get awesome!",
    "I am a tornado of death and bullets!",
    "Stop me before I kill again, except don't!",
    "Hehehehe, mwaa ha ha ha, MWAA HA HA HA!",
    "You call yourself a badass?",
    "Wow, did I really do that?",
    "Can, can I open my eyes now?",
    "Aww! Now I want a snow cone.",
    "Take a chill pill!",
    "Cryo me a river!",
    "Freeze! I don't know why I said that.",
    "Don't cryo!",
    "Frigid.",
    "Solid! Get it? As in frozen?",
    "Icely done.",
    "My assets... frozen!",
    "I can't feel my fingers! Gah! I don't have any fingers!",
    "Too cold... can't move!",
    "I am a robot popsicle!",
    "Brrh... So cold... brrh...",
    "Metal gears... frozen solid!",
    "Flesh fireworks!",
    "Oh, quit falling to pieces.",
    "Is that what people look like inside?",
    "Ooh, squishy bits!",
    "Meat confetti!",
    "Huh, robot's don't do that.",
    "This time it'll be awesome, I promise!"
    "Hey everybody, check out my package!",
    "Defragmenting!",
    "Recompiling my combat code!",
    "Running the sequencer!",
    "It's happening... it's happening!",
    "It's about to get magical!",
    "What will he do next?",
    "Things are about to get awesome!",
    "Let's get this party started!",
    "Glitchy weirdness is term of endearment, right?",
    "Push this button, flip this dongle, voila! Help me!"
]

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

class Commands:
    @matches(r'\/salute ?(?P<name>[^\s]+)?')
    def salute(self, message, name=None):
        if name is None:
            name = 'You'
        chat_id = message['chat']['id']
        sendMessage(chat_id, 'Hi {}'.format(name))

    @matches(r'\/quote(.+)?')
    def quote(self, message):
        chat_id = message['chat']['id']
        sendMessage(chat_id, choice(quotes))

    @matches(r'^\/sticker (?P<phrase>.*)$')
    def sticker(self, message, phrase):
        chat_id = message['chat']['id']
        if phrase not in stickers.keys():
            return
        sendSticker(chat_id, stickers[phrase])

    @classmethod
    def process(cls, update):
        if 'message' not in update.keys():
            return
        message = update['message']
        if 'text' in message.keys():
            text = message['text']
            methods = [getattr(cls, method) for method in dir(cls) if callable(getattr(cls, method)) and hasattr(getattr(cls, method), 'match')]
            candidates = [m for m in methods if m.match(text) is not False]
            if len(candidates) == 1:
                method = candidates.pop()
                params = method.match(text)
                return method(cls, message, **params)