from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from prettytable import PrettyTable

from pynote import config
from pynote import container


class Table(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _create_table(self):
        pass

    def __bool__(self):
        if self.table.get_string():
            return True
        else:
            return False

    def __str__(self):
        return self.table.get_string()


class DataTable(Table):

    def __init__(self, tags=[]):
        self.data = container.Data()
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
                    if tag in note:
                        table.add_row([key, title, updated])
                        break
            else:
                table.add_row([key, title, updated])

        return table


class TrashTable(container.Trash):

    def __init__(self):
        self.data = container.Trash()
        self.table = self._create_table()

    def _create_table(self):
        table = PrettyTable(['id', 'title', 'deleted'], print_empty=False)
        table.sortby = 'deleted'
        table.align = 'l'
        table.reversesort = True

        for key, note in enumerate(self.data):
            title = note.title
            deleted = note.deleted.strftime(config.DATEFORMAT)
            table.add_row([key, title, deleted])

        return table


class RevisionsTable(Table):

    def __init__(self, note):
        self.revisions = container.Revisions()
        self.note = note
        self.table = self._create_table()

    def _create_table(self):
        table = PrettyTable(['revision', 'title', 'updated'], print_empty=False)
        table.align = 'l'
        table.sortby = 'revision'
        table.reversesort = True

        # Search revisions and append them to self.notes.
        self.notes = [v for v in self.revisions if v.uuid == self.note.uuid]
        self.notes.append(self.note)

        # Fill table with data.
        for v in self.notes:
            updated = v.updated.strftime(config.DATEFORMAT)
            table.add_row([v.revision, v.title, updated])

        return table

    def __len__(self):
        return len(self.notes)
