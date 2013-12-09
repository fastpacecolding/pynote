from prettytable import PrettyTable
from datetime import datetime

from pynote.container import Data


class TableReport(Data):

    def __init__(self):
        super().__init__()
        self.list()

    def list(self):
        table = PrettyTable(['id', 'title', 'updated'])
        table.sortby = 'updated'
        table.align = 'l'
        table.reversesort = True

        for key, note in self.data.items():
            title = note.title
            updated = datetime.fromtimestamp(note.updated)
            updated = updated.strftime('%Y-%m-%d %H:%M')

            table.add_row([key, title, updated])

        self.table = table

    def __str__(self):
        return self.table.get_string()
