import os.path
from pathlib import Path
from datetime import datetime

from babel.dates import format_timedelta
from babel.dates import format_datetime

from pynote import config


class Notes:
    def __init__(self):
        self.path = Path(config.DATA)
        self.data = [Note(f) for f in self.path.iterdir()
                     if f.is_file() and f.suffix != '.json']
        self.data = sorted(self.data, key=lambda n: n.age)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            raise

    def __setitem__(self, key, value):
        try:
            if isinstance(value, Note):
                self.data[key] = value
                self.data[key].update()
            else:
                raise AttributeError('You can only assign Note objects!')
        except IndexError:
            raise

    def __delitem__(self, key):
        try:
            self.data[key].unlink()
            del self.data[key]
        except IndexError:
            raise

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)


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
