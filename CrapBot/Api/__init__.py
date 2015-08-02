import requests
from io import BufferedReader
from CrapBot import Config


def _camel_case(text):
    return "".join(x.title() if text.index(x) != 0 else x for x in text.split("_"))


def get(fn):
    _api_url = 'https://api.telegram.org/bot{}/{}'.format(Config.token, _camel_case(fn.__name__))

    def do_get(*args, **kwargs):
        params = fn(*args, **kwargs)
        r = requests.get(_api_url, params=params)
        return r.json()

    return do_get


def post(fn):
    _api_url = 'https://api.telegram.org/bot{}/{}'.format(Config.token, _camel_case(fn.__name__))

    def do_post(*args, **kwargs):
        params, files = fn(*args, **kwargs)
        print(params)
        print(files)
        r = requests.post(_api_url, params=params, files=files)
        return r.json()

    return do_post


@get
def get_me():
    return None


@get
def send_message(identifier, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': identifier,
        'text': text
    }
    if disable_web_page_preview is not None:
        params['disable_web_page_preview'] = disable_web_page_preview
    if reply_to_message_id is not None:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        params['reply_markup'] = reply_markup.json()

    return params


@get
def forward_message(identifier, from_id, msg_id):
    return {
        'chat_id': identifier,
        'from_chat_id': from_id,
        'message_id': msg_id
    }


@post
def send_photo(identifier, photo, caption=None, reply_id=None, markup=None):
    files = None
    params = {'chat_id': identifier}
    if not isinstance(photo, BufferedReader):
        params['photo'] = photo
    else:
        files = {'photo': photo}
    if caption is not None:
        params['caption'] = caption
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params, files


@post
def send_audio(identifier, audio, reply_id=None, markup=None):
    files = None
    params = {'chat_id': identifier}
    if not isinstance(audio, BufferedReader):
        params['audio'] = audio
    else:
        files = {'audio': audio}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params, files


@post
def send_document(identifier, document, reply_id=None, markup=None):
    files = None
    params = {'chat_id': identifier}
    if not isinstance(document, BufferedReader):
        params['document'] = document
    else:
        files = {'document': document}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params, files


@post
def send_sticker(identifier, sticker, reply_id=None, markup=None):
    files = None
    params = {'chat_id': identifier}
    if not isinstance(sticker, BufferedReader):
        params['sticker'] = sticker
    else:
        files = {'sticker': sticker}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params, files


@post
def send_video(identifier, video, reply_id=None, markup=None):
    files = None
    params = {'chat_id': identifier}
    if not isinstance(video, BufferedReader):
        params['video'] = video
    else:
        files = {'video': video}
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params, files


@get
def send_location(identifier, latitude, longitude, reply_id=None, markup=None):
    params = {
        'chat_id': identifier,
        'latitude': latitude,
        'longitude': longitude
    }
    if reply_id is not None:
        params['reply_to_message_id'] = reply_id
    if markup is not None:
        params['reply_markup'] = markup.json()
    return params


_available_actions = [
    'typing', 'upload_photo', 'record_video',
    'upload_video', 'record_audio', 'upload_audio',
    'upload_document', 'find_location'
]


@get
def send_chat_action(identifier, action):
    if action not in _available_actions:
        raise Exception
    return {
        'chat_id': identifier,
        'action': action
    }


@get
def get_user_profile_photos(identifier, offset=None, limit=None):
    params = {
        'user_id': identifier
    }
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    return params


@get
def get_updates(offset=None, limit=None, timeout=None):
    params = {}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if timeout is not None:
        params['timeout'] = timeout
    return params


@get
def set_webhook(url=None):
    params = {}
    if url is not None:
        params['url'] = url
    return params
