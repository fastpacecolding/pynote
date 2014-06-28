import os.path
from pathlib import Path
from datetime import datetime

from babel.dates import format_timedelta
from babel.dates import format_datetime

from pynote import config


def load_notes():
    path = Path(config.DATA)
    data = [Note(f) for f in path.iterdir()
            if f.is_file() and f.suffix not in config.IGNORE_EXTENSIONS]
    return sorted(data, key=lambda n: n.age)


# TODO: content should be a property
class Note:

    def __init__(self, path):
        self.path = path
        self.title = path.stem
        # Get content, if the file is not present create an empty one.
        if not path.exists():
            path.touch()
            self.content = ''
        else:
            with path.open('br') as f:
                self.content = f.read()

        # Check whether the note is encrypted or not.
        # It is indicated by the first suffix: my-note.crypt.txt
        if path.suffixes:
            if path.suffixes[0] == '.crypt':
                self.is_encrypted = True
            else:
                self.is_encrypted = False
        else:
            self.is_encrypted = False

        self.updated = self._getmtime()
        self.age = self._calc_age()

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

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

    def update(self):
        with self.path.open('w') as f:
            f.write(self.content)
        self.__init__(self.path)

    def get_header(self):
        return '{} @ {}, {} ago'.format(self.title, self.format_updated(),
                                        self.format_age())

    def _calc_age(self):
        return datetime.now() - self.updated

    def format_age(self):
        return format_timedelta(self.age, locale=config.LOCALE)

    def format_updated(self):
        return format_datetime(self.updated, format=config.DATEFORMAT,
                               locale=config.LOCALE)

    def _getmtime(self):
        updated = os.path.getmtime(str(self.path))
        return datetime.fromtimestamp(updated)
