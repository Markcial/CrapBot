
import requests, re, os


def matches(pattern):
    def decorator(fn):
        def match(subject):
            expr = re.compile(pattern)
            matches = expr.match(subject)
            if matches:
                return matches.groupdict()
            return False
        fn._match = match
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


class Commands:
    @matches(r'\/help(.+)?')
    def help(self):
        return 'help'

    @matches(r'\/salute ?(?P<name>[^\s]+)?')
    def salute(self, name='You'):
        return 'Hi {}'.format(name)

    @matches(r'\/enviar ?(?P<what>[^\s]+)? ?(?P<whom>[^\s]+)?')
    def enviar(self, what='Nothing', whom="Noone"):
        return 'Enviar un {} a {}'.format(what, whom)

    @classmethod
    def match(clss, text):
        methods = [getattr(clss, method) for method in dir(clss) if callable(getattr(clss, method)) and hasattr(getattr(clss, method), '_match')]
        candidates = [m for m in methods if m._match(text)]
        if len(candidates) > 1 or len(candidates) == 0:
            return clss.help(clss)
        method = candidates.pop()
        params = method._match(text)
        return method(clss, **params)


def setupWebhook():
    api = Api()
    api.setWebHook({'url': ''})