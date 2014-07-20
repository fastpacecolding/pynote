import os.path
import json
from pathlib import Path
from datetime import datetime
import click
from babel.dates import format_timedelta
from babel.dates import format_datetime
from pynote import config
from pynote.formatting import echo_error


def load_notes(path=Path(config.data)):
    if path.exists():
        data = [Note(f) for f in path.iterdir()
                if f.is_file() and (f.suffix not in config.ignore_extensions
                    and f.name != 'tags.json')]
        return sorted(data, key=lambda n: n.age)
    else:
        echo_error('Your data directory does not exist!')
        click.echo('Please create a data directory.')
        click.echo('You can do this with "mkdir {}".'.format(config.data))
        exit(1)


def get_note(data, key):
    if key < len(data):
        note = data[key]
        return note
    else:
        echo_error('This note does not exist!')
        exit(1)


def filter_tags(data, tag_str):
    # Avoid duplicates
    # http://stackoverflow.com/a/4230131/2587286
    seen = set()
    tag_list = tag_str.split()
    for i, note in enumerate(data):
        for tag in tag_list:
            if tag in note.tags and note not in seen:
                yield (i, note)
                seen.add(note)


class Note:

    tagfile = Path(config.data) / 'tags.json'

    def __init__(self, path):
        self.path = path
        self.title = path.stem
        # If the file is not present create an empty one.
        if not path.exists():
            path.touch()
        self.updated = self._getmtime()
        self.age = self._calc_age()
        self.is_encrypted = self._check_encrypted()

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

    @property
    def content(self):
        with self.path.open('br') as f:
            return f.read()

    @content.setter
    def content(self, value):
        with self.path.open('bw') as f:
            return f.write(value)

    @property
    def tags(self):
        if self.tagfile.exists():
            with self.tagfile.open() as f:
                tags = json.load(f)
            if self.title in tags:
                return tags[self.title]
            else:
                return []
        else:
            return []

    @tags.setter
    def tags(self, value):
        if self.tagfile.exists():
            with self.tagfile.open() as f:
                tags = json.load(f)
        else:
            self.tagfile.touch()
            tags = []
        tags[self.title] = value

        with self.tagfile.open('w') as f:
            json.dump(tags, f, indent=4)

    @classmethod
    def create(cls, title, encrypted=False):
        if config.extension and encrypted:
            filename = title + '.crypt' + config.extension
        elif config.extension and encrypted is False:
            filename = title + config.extension
        elif not config.extension and encrypted:
            filename = title + '.crypt'
        else:
            filename = title

        path = Path(os.path.join(config.DATA, filename))
        if path.exists():
            raise FileExistsError('Note already exists!')
        else:
            return cls(path)

    def format_header(self, colors=config.colors):
        header = '{} @ {}, {} ago'.format(self.title, self.format_updated(),
                                          self.format_age())
        header = click.style(header, bold=True) if colors else header
        if self.tags:
            header += '\n'
            header += ' / '.join(self.tags)
        return header

    def format_age(self):
        return format_timedelta(self.age, locale=config.locale)

    def format_updated(self):
        return format_datetime(self.updated, format=config.dateformat,
                               locale=config.locale)

    def _check_encrypted(self):
        # This is indicated by the first suffix: my-note.crypt.txt
        if self.path.suffixes:
            if self.path.suffixes[0] == '.crypt':
                return True
            else:
                return False
        else:
            return False

    def _getmtime(self):
        updated = os.path.getmtime(str(self.path))
        return datetime.fromtimestamp(updated)

    def _calc_age(self):
        return datetime.now() - self.updated
