import os
import os.path
import json

from pynote import container


class Exporter(container.Data):

    def __init__(self):
        super().__init__()
        self.cwd = os.path.join(os.getcwd(), 'pynote-export')

    def to_txt(self):
        os.mkdir(self.cwd)

        for note in self.data:
            with open(os.path.join(self.cwd, note.title), 'w') as f:
                f.write(note.content)

    def to_json(self):
        os.mkdir(self.cwd)

        for note in self.data:
            with open(os.path.join(self.cwd, note.title + '.json'), 'w') as f:
                f.write(note.to_json())
