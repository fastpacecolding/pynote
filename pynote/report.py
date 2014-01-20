from prettytable import PrettyTable
from datetime import datetime

from pynote import config
from pynote import container


class DataTable(container.Data):

    def __init__(self, tags=[]):
        super().__init__()
        self.tags = tags
        self.table = self._create_table()

    def _create_table(self):
        table = PrettyTable(['id', 'title', 'updated'], print_empty=False)
        table.sortby = 'updated'
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            updated = note.updated.strftime(config.DATEFORMAT)

            if self.tags:
                for tag in self.tags:
                    if note.has_tag(tag):
                        table.add_row([key, title, updated])
                        break
            else:
                table.add_row([key, title, updated])
        return table

    def __bool__(self):
        if self.table.get_string():
            return True
        else:
            return False

    def __str__(self):
        return self.table.get_string()


class TrashTable(container.Trash):

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
            deleted = note.deleted.strftime(config.DATEFORMAT)

            table.add_row([key, title, deleted])

        self.table = table

    def __str__(self):
        return self.table.get_string()

