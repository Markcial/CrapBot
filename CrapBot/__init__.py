
import requests, re, os
from random import choice


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


class Api(object):
    _api_url = 'https://api.telegram.org/bot{}/'
    _methods = [
        'getMe',
        'sendMessage',
        'forwardMessage',
        'sendPhoto',
        'sendAudio',
        'sendDocument',
        'sendSticker',
        'sendVideo',
        'sendLocation',
        'sendChatAction',
        'getUserProfilePhotos',
        'getUpdates',
        'setWebhook'
    ]

    def ep(self):
        token = os.environ['CRAP_BOT_TOKEN']
        return self._api_url.format(token)

    def get_api_method(self, method):
        url = self.ep() + method

        def call(params=None):
            if params is None:
                params = {}
            r = requests.get(url, params=params)
            return r.json()
        return call

    def __getattr__(self, name):
        if name in self._methods:
            return self.get_api_method(name)
        raise AttributeError('{} instance has no attribute {}'.format(self.__class__, name))

quotes = [
    'Hi there minion, what do you want?',
    'Hi there minion, i need you to get rid of those skags!',
]


class Commands:
    api = None
    @matches(r'\/help(.+)?')
    def help(self, message):
        chat_id = message['chat']['id']
        self.apiCall('sendMessage', {'chat_id': chat_id, 'text': 'Help message'})

    @matches(r'\/salute ?(?P<name>[^\s]+)?')
    def salute(self, message, name=None):
        if name is None:
            name = 'You'
        chat_id = message['chat']['id']
        self.apiCall('sendMessage', {'chat_id': chat_id, 'text': 'Hi {}'.format(name)})

    @matches(r'\/quote(.+)?')
    def quote(self, message):
        chat_id = message['chat']['id']
        self.apiCall('sendMessage', {'chat_id': chat_id, 'text': choice(quotes)})

    @matches(r'\/foo ?(?P<name>[^\s]+)?')
    def foo(self, message, name=None):
        if name is None:
            name = 'Bar'
        chat_id = message['chat']['id']
        self.apiCall('sendMessage', {'chat_id': chat_id, 'text': 'Spam spam spam spam spam {}'.format(name)})

    @classmethod
    def apiCall(cls, method, params):
        if cls.api is None:
            cls.api = Api()
        method = getattr(cls.api, method)
        return method(params)

    @classmethod
    def process(cls, update):
        if 'message' not in update.keys():
            return
        print(update)
        message = update['message']
        text = message['text']
        methods = [getattr(cls, method) for method in dir(cls) if callable(getattr(cls, method)) and hasattr(getattr(cls, method), 'match')]
        candidates = [m for m in methods if m.match(text)]
        if len(candidates) > 1 or len(candidates) == 0:
            return cls.help(cls, message)
        method = candidates.pop()
        params = method.match(text)
        return method(cls, message, **params)