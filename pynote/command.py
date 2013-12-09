import os
import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile

from pynote import config
from pynote import container


def new(title):
    now = datetime.now()
    data = container.Data()
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()

    note = container.Note.create(title)

    subprocess.call([config.EDITOR, tmp_file.name])
    with open(tmp_file.name, 'r') as f:
        note.content = f.read()

    data.append(note)
    os.remove(tmp_file.name)  # cleanup temporary file

    return note


def show(key):
    data = container.Data()
    print(data[key])


def delete(key):
    now = datetime.now()
    data = container.Data()
    trash = container.Trash()
    versions = container.Versions()
    note = data[key]

    versions.append(note)
    note.deleted = now.timestamp()
    note.revision += 1

    trash.append(note)
    del data[key]


def edit(key):
    now = datetime.now()
    data = container.Data()
    versions = container.Versions()
    note = data[key]
    versions.append(note)
    note.updated = now.timestamp()
    note.revision += 1
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()

    with open(tmp_file.name, 'w') as f:
        f.write(note.content)

    subprocess.call([config.EDITOR, tmp_file.name])

    with open(tmp_file.name, 'r') as f:
        note.content = f.read()

    data[key] = note
    os.remove(tmp_file.name)

    return note
