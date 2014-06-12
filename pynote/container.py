import os.path
from pathlib import Path
from datetime import datetime

from babel.dates import format_timedelta
from babel.dates import format_datetime

from pynote import config


def load_notes():
    path = Path(config.DATA)
    data = [Note(f) for f in path.iterdir()
            if f.is_file() and f.suffix != '.json']
    return sorted(data, key=lambda n: n.age)


class Note:

    def __init__(self, path):
        self.path = path
        self.title = path.name
        if path.exists():
            with path.open() as f:
                self.content = f.read()
        else:
            path.touch()
        self.updated = self._getmtime()
        self.age = self._calc_age()

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

    @classmethod
    def create(cls, title):
        path = Path(os.path.join(config.DATA, title))
        if path.exists():
            raise FileExistsError()
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
        now = datetime.now()
        age = now - self.updated
        return age

    def format_age(self):
        return format_timedelta(self.age, locale=config.LOCALE)

    def format_updated(self):
        return format_datetime(self.updated, format=config.DATEFORMAT,
                               locale=config.LOCALE)

    def _getmtime(self):
        updated = os.path.getmtime(str(self.path))
        return datetime.fromtimestamp(updated)
