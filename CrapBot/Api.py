import os
import requests
from io import BufferedReader

token = os.environ['CRAP_BOT_TOKEN']

def get(fn):
    _api_url = 'https://api.telegram.org/bot{}/{}'.format(token, fn.__name__)

    def do_get(*args,**kwargs):
        params = fn(*args, **kwargs)
        r = requests.get(_api_url, params=params)
        return r.json()
    return do_get

def post(fn):
    _api_url = 'https://api.telegram.org/bot{}/{}'.format(token, fn.__name__)

    def do_post(*args,**kwargs):
        params, files = fn(*args, **kwargs)
        print(params)
        print(files)
        r = requests.post(_api_url, params=params, files=files)
        return r.json()
    return do_post

@get
def getMe():
    return None

@get
def sendMessage(id, text):
    return {
        'chat_id': id,
        'text': text
    }

@get
def forwardMessage(id, from_id, msg_id):
    return {
        'chat_id': id,
        'from_chat_id': from_id,
        'message_id': msg_id
    }

@post
def sendPhoto(id, photo, caption=None, reply_id=None, markup=None):
    files = None
    params = {'chat_id': id}
    if not isinstance(photo, BufferedReader):
        params['photo'] = photo
    else:
        files = {'photo': photo}
    if caption is not None:
        params['caption'] = caption
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return (params, files)

@post
def sendAudio(id, audio, reply_id=None, markup=None):
    files = None
    params = {'chat_id': id}
    if not isinstance(audio, BufferedReader):
        params['audio'] = audio
    else:
        files = {'audio': audio}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return (params, files)

@post
def sendDocument(id, document, reply_id=None, markup=None):
    files = None
    params = {'chat_id': id}
    if not isinstance(document, BufferedReader):
        params['document'] = document
    else:
        files = {'document': document}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return (params, files)

@post
def sendSticker(id, sticker, reply_id=None, markup=None):
    files = None
    params = {'chat_id': id}
    if not isinstance(sticker, BufferedReader):
        params['sticker'] = sticker
    else:
        files = {'sticker': sticker}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return (params, files)

@post
def sendVideo(id, video, reply_id=None, markup=None):
    files = None
    params = {'chat_id': id}
    if not isinstance(video, BufferedReader):
        params['video'] = video
    else:
        files = {'video': video}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return (params, files)

@get
def sendLocation(id, latitude, longitude, reply_id=None, markup=None):
    params = {
        'chat_id': id,
        'latitude': latitude,
        'longitude': longitude
    }
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup
    return params

_available_actions = [
    'typing', 'upload_photo', 'record_video',
    'upload_video', 'record_audio', 'upload_audio',
    'upload_document','find_location'
]

@get
def sendChatAction(id, action):
    if action not in _available_actions:
        raise Exception
    return {
        'chat_id': id,
        'action': action
    }

@get
def getUserProfilePhotos(id, offset=None, limit=None):
    params = {
        'user_id': id
    }
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    return params

@get
def getUpdates(offset=None, limit=None, timeout=None):
    params = {}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if timeout is not None:
        params['timeout'] = timeout
    return params

@get
def setWebhook(url=None):
    params = None
    if url is not None:
        params['url'] = url
    return params