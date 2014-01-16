from prettytable import PrettyTable
from datetime import datetime

from pynote import config
from pynote.container import Data
from pynote.container import Trash


class DataTable(Data):

    def __init__(self):
        super().__init__()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'updated', 'timestamp'])
        table.sortby = 'timestamp'  # fixes a sorting issue, see #302
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            updated = note.updated.strftime(config.DATEFORMAT)
            timestamp = note.updated.timestamp()

            table.add_row([key, title, updated, timestamp])

        self.table = table

    def __str__(self):
        return self.table.get_string(fields=['id', 'title', 'updated'])


class TrashTable(Trash):

    def __init__(self):
        super().__init__()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'deleted', 'timestamp'])
        table.sortby = 'timestamp'  # fixes a sorting issue, see #302
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            deleted = note.deleted.strftime(config.DATEFORMAT)
            timestamp = note.deleted.timestamp()

            table.add_row([key, title, deleted, timestamp])

        self.table = table

    def __str__(self):
        return self.table.get_string(fields=['id', 'title', 'deleted'])

