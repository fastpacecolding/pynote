import re
import json
import uuid
import os.path
from datetime import datetime
from prettytable import PrettyTable

from pynote import config


class Data:
    """
    The main data container class for notes.

    The content of this container class maps to
    the data.json file.  Everything you append
    to an instance of this class will be serialised
    to json and written to data.json.

    """
    def __init__(self, data_file=config.DATA_FILE):
        self.data_file = data_file
        self.data = []
        self.load()

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
            self.refresh()
        except IndexError:
            raise

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            raise

    def __delitem__(self, key):
        try:
            del self.data[key]
            self.refresh()
        except IndexError:
            raise

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def append(self, note):
        self.data.append(note)
        self.refresh()

    def load(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f, cls=NoteJSONDecoder)
        except FileNotFoundError as e:
            print(_('Error: {} does not exist').format(self.data_file))
            print(_('Maybe you have to init pynote first.'))
            exit(1)

    def dump(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, cls=NoteJSONEncoder)

    def dumps(self):
        return json.dumps(self.data, cls=NoteJSONEncoder)

    def refresh(self):
        self.dump()
        self.load()


class Trash(Data):
    """
    A subclass of Data.

    This class maps to trash.json. The rest is
    similar to Data.

    """
    def __init__(self, trash_file=config.TRASH_FILE):
        self.data_file = trash_file
        self.data = []
        self.load()


class Revisions(Data):
    """
    A subclass of Data.

    This class maps to versions.json. The rest is
    similar to Data.

    """
    def __init__(self, revisions_file=config.REVISIONS_FILE):
        self.data_file = revisions_file
        self.data = []
        self.load()


class Note:
    """
    This class is used to represent a note.

    """
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
        note = cls(title=title, created=now, updated=now, deleted=None,
                   revision=1, uuid=str(uuid.uuid4()), tags=set(),
                   content='')

        return note

    @classmethod
    def from_dict(cls, d):
        created = datetime.fromtimestamp(d['created'])
        updated = datetime.fromtimestamp(d['updated'])
        deleted = datetime.fromtimestamp(d['deleted']) if d['deleted'] else None

        note = cls(title=d['title'], created=created,
                   updated=updated, deleted=deleted,
                   revision=d['revision'], uuid=d['uuid'],
                   tags=set(d['tags']), content=d['content'])

        return note

    def to_dict(self):
        created = self.created.timestamp()
        updated = self.updated.timestamp()
        deleted = self.deleted.timestamp() if self.deleted else None

        d = {'title': self.title, 'created': created,
             'updated': updated, 'deleted': deleted,
             'revision': self.revision, 'uuid': self.uuid,
             'tags': list(self.tags), 'content': self.content}

        return d

    def get_header(self):
        table = PrettyTable(header=False)
        table.add_row(['title', self.title])

        created = self.created.strftime(config.DATEFORMAT)
        table.add_row(['created', created])

        updated = self.updated.strftime(config.DATEFORMAT)
        table.add_row(['updated', updated])

        tags = sorted(self.tags)
        tags = format(tags) if tags else _('None')
        tags = re.sub('[\'\[\]]', '', tags)  # Strip '[]' and "'" chars.
        table.add_row(['tags', tags])

        table.add_row(['uuid', self.uuid])
        table.align = 'l'

        return table.get_string()

    def __contains__(self, tag):
        if tag in self.tags:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.uuid == other.uuid and self.revision == other.revision:
            return True
        else:
            return False

    def __str__(self):
        return self.content


class NoteJSONEncoder(json.JSONEncoder):
    """
    JSON Encoder class.  Used to serialise
    Note objects.

    """
    def default(self, o):
        try:
            note = o.to_dict()
        except TypeError:
            pass
        else:
            return note
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)


class NoteJSONDecoder(json.JSONDecoder):
    """
    JSON Decoder class.  Used to deserialise
    Note objects.

    """
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        return Note.from_dict(d)
