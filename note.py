import os
import os.path
import subprocess
import json
import uuid
import configparser
from prettytable import PrettyTable
from datetime import datetime
from tempfile import NamedTemporaryFile


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


class NotesContainerMixin:
    data_file = read_config()['data']
    # trash_file = read_config()['trash']
    # version_file = read_config()['versions']
    data = []
    # trash =
    # version =

    @classmethod
    def get_data(cls):
        with open(cls.data_file, 'r') as f:
            cls.data = json.load(f)

    def dump_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)

    def update_data(self):
        self.dump_data()
        self.get_data()


class TableReport(NotesContainerMixin):

    def __init__(self):
        self.get_data()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'updated'])
        table.sortby = 'updated'
        table.align = 'l'
        table.reversesort = True

        for note in self.data:
            uuid = note['uuid'][0:8]
            title = note['title']
            updated = datetime.fromtimestamp(note['updated'])
            updated = updated.strftime('%Y-%m-%d %H:%I')

            table.add_row([uuid, title, updated])

        self.table = table

    def __str__(self):
        return self.table.get_string()


class Note(NotesContainerMixin):

    def __init__(self, title, created, updated, uuid, tags, content):
        self.title = title
        self.created = created
        self.updated = updated
        self.uuid = uuid
        self.tags = tags
        self.content = content
        self.get_data()

    @classmethod
    def create(cls, title):
        now = datetime.now()
        tmp_file = NamedTemporaryFile(delete=False)
        tmp_file.close()

        note = cls(title=title,
                   created=now.timestamp(),
                   updated=now.timestamp(),
                   uuid=str(uuid.uuid4()),
                   tags='',
                   content='')

        subprocess.call(['nano', tmp_file.name])
        with open(tmp_file.name, 'r') as f:
            note.content = f.read()

        # Append the created note to the datacontainer
        # and update JSON file.
        cls.data.append(note.to_dict())
        note.update_data()
        os.remove(tmp_file.name)  # cleanup temporary file

        return note

    @classmethod
    def show(cls, uuid):
        cls.get_data()
        for note in cls.data:
            if uuid == note['uuid'][0:len(uuid)]:
                print(cls.from_dict(note))

    @classmethod
    def from_dict(cls, _dict):
        note = cls(title=_dict['title'],
                   created=_dict['created'],
                   updated=_dict['updated'],
                   uuid=_dict['uuid'],
                   tags=_dict['tags'],
                   content=_dict['content'])
        return note

    def to_dict(self):
        _dict = {'title': self.title,
                'created': self.created,
                'updated': self.updated,
                'uuid': self.uuid,
                'tags': self.tags,
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
                  '{4}\n').format(self.title,
                                  created,
                                  updated,
                                  self.uuid,
                                  self.content)
        return string
