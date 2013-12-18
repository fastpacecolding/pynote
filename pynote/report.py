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
        table = PrettyTable(['id', 'title', 'updated'])
        table.sortby = 'updated'
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            updated = datetime.fromtimestamp(note.updated)
            updated = updated.strftime(config.DATEFORMAT)

            table.add_row([key, title, updated])

        self.table = table

    def __str__(self):
        return self.table.get_string()


class TrashTable(Trash):

    def __init__(self):
        super().__init__()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'deleted'])
        table.sortby = 'deleted'
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            deleted = datetime.fromtimestamp(note.deleted)
            deleted = deleted.strftime(config.DATEFORMAT)

            table.add_row([key, title, deleted])

        self.table = table

    def __str__(self):
        return self.table.get_string()

