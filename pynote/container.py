import os.path
import json
import uuid
from json import JSONEncoder
from datetime import datetime

from pynote import config


class Data:

    def __init__(self):
        self.data_file = config.DATA_FILE
        self.data = []
        self.load()

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
            self.refresh()
        except IndexError:
            print('This note does not exist!')
            exit()

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            print('This note does not exist!')
            exit()

    def __delitem__(self, key):
        try:
            del self.data[key]
            self.refresh()
        except IndexError:
            print('This note does not exist!')
            exit()

    def __iter__(self):
        return iter(self.data)

    def append(self, note):
        self.data.append(note)
        self.refresh()

    def load(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)

        for note in data:
            self.data.append(Note.from_dict(note))

    def dump(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, cls=NoteJSONEncoder)

    def dumps(self):
        return json.dumps(self.data, cls=NoteJSONEncoder)

    def refresh(self):
        self.dump()
        self.load()


class Trash(Data):

    def __init__(self):
        self.data_file = config.TRASH_FILE
        self.data = []
        self.load()


class Versions(Data):

    def __init__(self):
        self.data_file = config.VERSIONS_FILE
        self.data = []
        self.load()


class Note:

    def __init__(self, title, created, updated, deleted,
                 revision, uuid, tags, content):
        self.title = title
        self.created = created
        self.updated = updated
        self.deleted = deleted
        self.revision = revision
        self.uuid = uuid
        self.tags = tags
        self.content = content

    @classmethod
    def create(cls, title):
        now = datetime.now()
        note = cls(title=title, created=now.timestamp(), updated=now.timestamp(),
                   deleted=None, revision=1, uuid=str(uuid.uuid4()), tags='',
                   content='')

        return note

    @classmethod
    def from_dict(cls, _dict):
        note = cls(title=_dict['title'], created=_dict['created'],
                   updated=_dict['updated'], deleted=_dict['deleted'],
                   revision=_dict['revision'], uuid=_dict['uuid'],
                   tags=_dict['tags'], content=_dict['content'])

        return note

    def to_dict(self):
        _dict = {'title': self.title, 'created': self.created,
                 'updated': self.updated, 'deleted': self.deleted,
                 'revision': self.revision, 'uuid': self.uuid,
                 'tags': self.tags, 'content': self.content}

        return _dict

    def __str__(self):
        created = datetime.fromtimestamp(self.created)
        created = created.strftime('%Y-%m-%d %H:%M')
        updated = datetime.fromtimestamp(self.updated)
        updated = updated.strftime('%Y-%m-%d %H:%M')

        string = ('+-------------------------------------------------+\n'
                  '| title:    {0}\n'
                  '| created:  {1}\n'
                  '| updated:  {2}\n'
                  '| revision: {3}\n'
                  '| uuid:     {4}\n'
                  '+-------------------------------------------------+\n'
                  '\n'
                  '{5}\n').format(self.title, created, updated, self.revision,
                                  self.uuid, self.content)
        return string


class NoteJSONEncoder(JSONEncoder):

    def default(self, o):
        try:
            note = o.to_dict()
        except TypeError:
            pass
        else:
            return note
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)
