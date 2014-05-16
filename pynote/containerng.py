import os.path
import io
from datetime import datetime
from pathlib import Path
from plaintable import Table

from pynote import config


class Notes:
    def __init__(self):
        self.path = Path(os.path.expanduser(config.DATA))
        self.data = [Note(f) for f in self.path.iterdir()
                     if (f.is_file() and f.suffix != '.json')]

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

    def __len(self):
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

    def update(self):
        with self.path.open('w') as f:
            f.write(self.content)
        self.__init__(self.path)

    def get_header(self):
        updated = self.updated.strftime(config.DATEFORMAT)
        s  = '{} @ {}'.format(self.title, updated)
        return s

    def _getmtime(self):
        updated = os.path.getmtime(str(self.path))
        return datetime.fromtimestamp(updated)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

