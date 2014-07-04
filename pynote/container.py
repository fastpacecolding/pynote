import os.path
import click
from pathlib import Path
from datetime import datetime
from babel.dates import format_timedelta
from babel.dates import format_datetime
from pynote import config
from pynote.formatting import echo_error


def load_notes(path=Path(config.DATA)):
    if path.exists():
        data = [Note(f) for f in path.iterdir()
                if f.is_file() and f.suffix not in config.IGNORE_EXTENSIONS]
        return sorted(data, key=lambda n: n.age)
    else:
        raise FileNotFoundError('Data directory does not exist!')


def get_note(data, key):
    try:
        note = data[key]
    except IndexError:
        echo_error('This note does not exist!')
        exit(1)
    return note


class Note:

    def __init__(self, path):
        self.path = path
        self.title = path.stem
        self._content = b''
        # If the file is not present create an empty one.
        if not path.exists():
            path.touch()
        self.is_encrypted = self._check_encrypted()
        self.updated = self._getmtime()
        self.age = self._calc_age()

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

    @property
    def content(self):
        return self._read_content()

    @content.setter
    def content(self, value):
        self._content = value
        self._write_content()

    @classmethod
    def create(cls, title, encrypted=False):
        if config.EXTENSION and encrypted:
            filename = title + '.crypt' + config.EXTENSION
        elif config.EXTENSION and encrypted is False:
            filename = title + config.EXTENSION
        elif not config.EXTENSION and encrypted:
            filename = title + '.crypt'
        else:
            filename = title

        path = Path(os.path.join(config.DATA, filename))
        if path.exists():
            raise FileExistsError('Note already exists!')
        else:
            return cls(path)

    def get_header(self, styled=config.COLORS):
        header = '{} @ {}, {} ago'.format(self.title, self.format_updated(),
                                          self.format_age())
        header = click.style(header, bold=True) if styled else header
        return header

    def format_age(self):
        return format_timedelta(self.age, locale=config.LOCALE)

    def format_updated(self):
        return format_datetime(self.updated, format=config.DATEFORMAT,
                               locale=config.LOCALE)

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

    def _read_content(self):
        with self.path.open('br') as f:
            return f.read()

    def _write_content(self):
        with self.path.open('bw') as f:
            return f.write(self._content)
