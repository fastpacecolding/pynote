from datetime import datetime
import os.path
import re
import unicodedata
import click
from babel.dates import format_timedelta, format_datetime
from . import config

__version__ = '1.0.0'
__license__ = 'MIT'
__copyright__ = '(c) 2013-2016 Stefan Tatschner <rumpelsepp@sevenbyte.org>'


class Note:
    """
    Represents a note. A note object maps to a textfile
    somewhere in the filesystem. The note's title is maps
    to the filename and the updated attribute to the modification
    time.
    """
    def __init__(self, path):
        self.path = path
        self.title = path.stem
        self.slug = self._slugify(self.title)
        # If the file is not present create an empty one.
        if not path.exists():
            path.touch()
        self.updated = self._getmtime()
        self.age = self._calc_age()

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.path)

    @property
    def content(self):
        with self.path.open('r') as f:
            return f.read()

    @content.setter
    def content(self, value):
        with self.path.open('w') as f:
            return f.write(value)

    @classmethod
    def create(cls, title, encrypted=False):
        if config.EXTENSION:
            filename = title + config.EXTENSION
        else:
            filename = title

        path = config.DATA_PATH / filename
        if path.exists():
            raise FileExistsError('Note already exists!')
        else:
            return cls(path)

    def update_path(self, path):
        """
        When self.path is updated the note object needs to
        be reinitialized. So let's wrap the constructor!
        """
        self.__init__(path)

    def format_header(self, colors=config.COLORS):
        header = '{} @ {}, {} ago'.format(
            self.title,
            self.format_updated(),
            self.format_age()
        )
        return click.style(header, bold=True) if colors else header

    def format_age(self):
        return format_timedelta(self.age, locale=config.LOCALE)

    def format_updated(self):
        return format_datetime(
            self.updated,
            format=config.DATEFORMAT,
            locale=config.LOCALE
        )

    def _getmtime(self):
        updated = os.path.getmtime(str(self.path))
        return datetime.fromtimestamp(updated)

    def _calc_age(self):
        return datetime.now() - self.updated

    @staticmethod
    def _slugify(value):
        # stolen from Django: django/utils/text.py
        value = unicodedata.normalize('NFKD', value)
        value = value.encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)
