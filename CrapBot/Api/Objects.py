import json


class Json(object):
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class Element(object):
    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__


class Update(Element):
    def __init__(self, identifier, msg):
        self.identifier = identifier
        self.message = Message(
            msg['message_id'],
            msg['from'],
            msg['date'],
            msg['chat'],
            forward_from=msg['forward_from'] if 'forward_from' in msg else None,
            forward_date=msg['forward_date'] if 'forward_date' in msg else None,
            reply_to_message=msg['reply_to_message'] if 'reply_to_message' in msg else None,
            text=msg['text'] if 'text' in msg else None,
            audio=msg['audio'] if 'audio' in msg else None,
            document=msg['document'] if 'document' in msg else None,
            photo=msg['photo'] if 'photo' in msg else None,
            sticker=msg['sticker'] if 'sticker' in msg else None,
            video=msg['video'] if 'video' in msg else None,
            caption=msg['caption'] if 'caption' in msg else None,
            contact=msg['contact'] if 'contact' in msg else None,
            location=msg['location'] if 'location' in msg else None,
            new_chat_participant=msg['new_chat_participant'] if 'new_chat_participant' in msg else None,
            left_chat_participant=msg['left_chat_participant'] if 'left_chat_participant' in msg else None,
            new_chat_title=msg['new_chat_title'] if 'new_chat_title' in msg else None,
            new_chat_photo=msg['new_chat_photo'] if 'new_chat_photo' in msg else None,
            delete_chat_photo=msg['delete_chat_photo'] if 'delete_chat_photo' in msg else None,
            group_chat_created=msg['group_chat_created'] if 'group_chat_created' in msg else None
        )


class Message(Element):
    def __init__(self, identifier, whom, date, chat, forward_from=None, forward_date=None,
                 reply_to_message=None, text=None, audio=None, document=None, photo=None,
                 sticker=None, video=None, caption=None, contact=None, location=None,
                 new_chat_participant=None, left_chat_participant=None, new_chat_title=None,
                 new_chat_photo=None, delete_chat_photo=None, group_chat_created=None):
        self.identifier = identifier
        setattr(self, 'from', User(
            whom['id'],
            whom['first_name'],
            last_name=whom['last_name'] if 'last_name' in whom else None,
            username=whom['username'] if 'username' in whom else None
        ))
        self.date = date
        if 'first_name' in chat:
            self.chat = User(
                chat['id'],
                chat['first_name'],
                last_name=chat['last_name'] if 'last_name' in chat else None,
                username=chat['username'] if 'username' in chat else None
            )
        else:
            self.chat = GroupChat(
                chat['id'],
                chat['title']
            )
        if forward_from is not None:
            self.forward_from = User(
                forward_from['id'],
                forward_from['first_name'],
                last_name=forward_from['last_name'] if 'last_name' in forward_from else None,
                username=forward_from['username'] if 'username' in forward_from else None
            )
        if forward_date is not None:
            self.forward_date = forward_date
        if reply_to_message is not None:
            args = {k:v for k,v in reply_to_message.items() if k not in ('message_id', 'from', 'date', 'chat')}
            self.reply_to_message = Message(
                reply_to_message['message_id'],
                reply_to_message['from'],
                reply_to_message['date'],
                reply_to_message['chat'],
                **args
            )
        if text is not None:
            self.text = text
        if audio is not None:
            self.audio = Audio(
                audio['file_id'],
                audio['duration'],
                mime_type=audio['mime_type'] if 'mime_type' in audio else None,
                file_size=audio['file_size'] if 'file_size' in audio else None
            )
        if document is not None:
            self.document = Document(
                document['file_id'],
                thumb=document['thumb'] if 'thumb' in document else None,
                file_name=document['file_name'] if 'file_name' in document else None,
                mime_type=document['mime_type'] if 'mime_type' in document else None,
                file_size=document['file_size'] if 'file_size' in document else None
            )
        if photo is not None:
            self.photo = [PhotoSize(
                ph['file_id'],
                ph['width'],
                ph['height'],
                file_size=ph['file_size'] if 'file_size' in ph else None
            ) for ph in photo]
        if sticker is not None:
            self.sticker = Sticker(
                sticker['file_id'],
                sticker['width'],
                sticker['height'],
                thumb=sticker['thumb'] if 'thumb' in sticker else None,
                file_size=sticker['file_size'] if 'file_size' in sticker else None
            )
        if video is not None:
            self.video = Video(
                video['file_id'],
                video['width'],
                video['height'],
                video['duration'],
                thumb=video['thumb'] if 'thumb' in video else None,
                mime_type=video['mime_type'] if 'mime_type' in video else None,
                file_size=video['file_size'] if 'file_size' in video else None,
            )
        if caption is not None:
            self.caption = caption
        if contact is not None:
            self.contact = Contact(
                contact['phone_number'],
                contact['fist_name'],
                last_name=contact['last_name'] if 'last_name' in contact else None,
                user_id=contact['user_id'] if 'user_id' in contact else None
            )
        if location is not None:
            self.location = Location(
                location['longitude'],
                location['latitude']
            )
        if new_chat_participant is not None:
            self.new_chat_participant = User(
                new_chat_participant['id'],
                new_chat_participant['first_name'],
                last_name=new_chat_participant['last_name'] if 'last_name' in new_chat_participant else None,
                username=new_chat_participant['username'] if 'username' in new_chat_participant else None
            )
        if left_chat_participant is not None:
            self.left_chat_participant = User(
                left_chat_participant['id'],
                left_chat_participant['first_name'],
                last_name=left_chat_participant['last_name'] if 'last_name' in left_chat_participant else None,
                username=left_chat_participant['username'] if 'username' in left_chat_participant else None
            )
        if new_chat_title is not None:
            self.new_chat_title = new_chat_title
        if new_chat_photo is not None:
            self.new_chat_photo = [PhotoSize(
                ph['file_id'],
                ph['width'],
                ph['height'],
                file_size=ph['file_size'] if 'file_size' in ph else None
            ) for ph in new_chat_photo]
        if delete_chat_photo is not None:
            self.delete_chat_photo = delete_chat_photo
        if group_chat_created is not None:
            self.group_chat_created = group_chat_created

    @property
    def type(self):
        for attr in ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'contact', 'location']:
            if hasattr(self, attr):
                return attr

        for attr in ['new_chat_participant', 'left_chat_participant', 'new_chat_title',
                     'new_chat_photo', 'delete_chat_photo', 'group_chat_created']:
            if hasattr(self, attr):
                return 'roster'

        return 'unknown'

class User(Element):
    def __init__(self, identifier, first_name, last_name=None, username=None):
        self.identifier = identifier
        self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if username is not None:
            self.username = username


class GroupChat(Element):
    def __init__(self, identifier, title):
        self.identifier = identifier
        self.title = title


class PhotoSize(Element):
    def __init__(self, identifier, width, height, file_size=None):
        self.identifier = identifier
        self.width = width
        self.height = height
        if file_size is not None:
            self.file_size = file_size


class Audio(Element):
    def __init__(self, identifier, duration, mime_type=None, file_size=None):
        self.identifier = identifier
        self.duration = duration
        if mime_type is not None:
            self.mime_type = mime_type
        if file_size is not None:
            self.file_size = file_size


class Document(Element):
    def __init__(self, identifier, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.identifier = identifier
        if thumb is not None:
            self.thumb = PhotoSize(
                thumb['file_id'],
                thumb['width'],
                thumb['height'],
                file_size=thumb['file_size'] if 'file_size' in thumb else None
            )
        if file_name is not None:
            self.file_name = file_name
        if mime_type is not None:
            self.mime_type = mime_type
        if file_size is not None:
            self.file_size = file_size


class Sticker(Element):
    def __init__(self, identifier, width, height, thumb=None, file_size=None):
        self.identifier = identifier
        self.width = width
        self.height = height
        if thumb is not None:
            self.thumb = PhotoSize(
                thumb['file_id'],
                thumb['width'],
                thumb['height'],
                file_size=thumb['file_size'] if 'file_size' in thumb else None
            )
        if file_size is not None:
            self.file_size = file_size


class Video(Element):
    def __init__(self, identifier, width, height, duration, thumb=None, mime_type=None, file_size=None):
        self.identifier = identifier
        self.width = width
        self.height = height
        self.duration = duration
        if thumb is not None:
            self.thumb = PhotoSize(
                thumb['file_id'],
                thumb['width'],
                thumb['height'],
                file_size=thumb['file_size'] if 'file_size' in thumb else None
            )
        if mime_type is not None:
            self.mime_type = mime_type
        if file_size is not None:
            self.file_size = file_size


class Contact(Element):
    def __init__(self, phone_number, first_name, last_name=None, user_id=None):
        self.phone_number = phone_number
        self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if user_id is not None:
            self.user_id = user_id


class Location(Element):
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class UserProfilePhotos(Element):
    def __init__(self, total_count, photos):
        self.total_count = total_count
        self.photos = [[PhotoSize(
            ph['file_id'],
            ph['width'],
            ph['height'],
            file_size=ph['file_size'] if 'file_size' in ph else None
        ) for ph in c] for c in photos]

class ReplyKeyboardMarkup(Json):
    def __init__(self, keyboard, resize_keyboard=None, one_time_keyboard=None, selective=None):
        self.keyboard = keyboard
        if resize_keyboard is not None:
            self.resize_keyboard = resize_keyboard
        if one_time_keyboard is not None:
            self.one_time_keyboard = one_time_keyboard
        if selective is not None:
            self.selective = selective


class ReplyKeyboardHide(Json):
    def __init__(self, selective=None):
        self.hide_keyboard = True
        if selective is not None:
            self.selective = selective


class ForceReply(Json):
    def __init__(self, selective=None):
        self.force_reply = True
        if selective is not None:
            self.selective = selective