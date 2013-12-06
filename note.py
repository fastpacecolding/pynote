import os
import os.path
import subprocess
import json
from json import JSONEncoder
import uuid
import configparser
from prettytable import PrettyTable
from datetime import datetime
from tempfile import NamedTemporaryFile
from pprint import pprint


def read_config():
    config = configparser.ConfigParser()
    config.read('notesrc')

    data_file = config['paths']['data']
    data_file = os.path.expanduser(data_file)
    trash_file = config['paths']['trash']
    trash_file = os.path.expanduser(trash_file)
    versions_file = config['paths']['versions']
    versions_file = os.path.expanduser(versions_file)

    return {'data': data_file, 'trash': trash_file, 'versions': versions_file}


class Data:

    def __init__(self):
        self.data_file = read_config()['data']
        self.data = {}
        self.load()

    def add(self, note):
        keys = [int(key) for key in self.data.keys()]
        key = max(keys) + 1 if keys else 1
        key = str(key)
        self.data[key] = note
        self.refresh()

    def update(self, key, note):
        self.data[key] = note
        self.refresh()

    def delete(self, key):
        del self.data[key]
        self.refresh()

    def load(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)

        for key, note in data.items():
            self.data[key] = Note.from_dict(note)

    def dump(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, cls=NoteJSONEncoder)

    def refresh(self):
        self.dump()
        self.load()


class Trash(Data):

    def __init__(self):
        super().__init__()
        self.data_file = read_config()['trash']


class Versions(Data):

    def __init__(self):
        super().__init__()
        self.data_file = read_config()['versions']


class Note:

    def __init__(self, title, created, updated, uuid, tags, content):
        self.title = title
        self.created = created
        self.updated = updated
        # self.deleted = deleted
        self.uuid = uuid
        self.tags = tags
        self.content = content

    @classmethod
    def create(cls, title):
        now = datetime.now()
        note = cls(title=title, created=now.timestamp(), updated=now.timestamp(),
                   uuid=str(uuid.uuid4()), tags='', content='')

        return note

    @classmethod
    def from_dict(cls, _dict):
        note = cls(title=_dict['title'], created=_dict['created'],
                   updated=_dict['updated'], uuid=_dict['uuid'],
                   tags=_dict['tags'], content=_dict['content'])

        return note

    def to_dict(self):
        _dict = {'title': self.title, 'created': self.created,
                 'updated': self.updated, 'uuid': self.uuid, 'tags': self.tags,
                 'content': self.content}

        return _dict

    def __str__(self):
        created = datetime.fromtimestamp(self.created)
        created = created.strftime('%Y-%m-%d %H:%I')
        updated = datetime.fromtimestamp(self.updated)
        updated = updated.strftime('%Y-%m-%d %H:%I')

        string = ('title:   {0}\n'
                  'created: {1}\n'
                  'updated: {2}\n'
                  'uuid:    {3}\n'
                  '\n'
                  '---------------------------------------------\n'
                  '{4}\n').format(self.title, created, updated, self.uuid,
                                  self.content)
        return string


class TableReport(Data):

    def __init__(self):
        super().__init__()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'updated'])
        table.sortby = 'updated'
        table.align = 'l'
        table.reversesort = True

        for k, v in self.data.items():
            _id = k
            title = v.title
            updated = datetime.fromtimestamp(v.updated)
            updated = updated.strftime('%Y-%m-%d %H:%I')

            table.add_row([_id, title, updated])

        self.table = table

    def __str__(self):
        return self.table.get_string()


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


def new_note(title):
    now = datetime.now()
    container = Data()
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()

    note = Note.create(title)

    subprocess.call(['nano', tmp_file.name])
    with open(tmp_file.name, 'r') as f:
        note.content = f.read()

    container.add(note)
    os.remove(tmp_file.name)  # cleanup temporary file

    return note


def show_note(key):
    container = Data()
    # TODO: write accessor or something similar...
    print(container.data[key])


def delete_note(key):
    data = Data()
    trash = Trash()

    trash.add(data.data[key])
    data.delete(key)
