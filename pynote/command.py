import os
import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile
import difflib

from pynote import config
from pynote import container
from pynote import helper
from pynote import report


def new(title):
    data = container.Data()
    tmp_file = helper.create_tempfile()
    note = container.Note.create(title)

    subprocess.call([config.EDITOR, tmp_file])
    with open(tmp_file, 'r') as f:
        note.content = f.read()

    data.append(note)
    os.remove(tmp_file)  # cleanup temporary file


def show(key):
    data = container.Data()
    print(data[key])


def delete(key):
    now = datetime.now().timestamp()
    data = container.Data()
    trash = container.Trash()
    versions = container.Versions()
    note = data[key]

    versions.append(note)
    note.deleted = now
    note.revision += 1

    trash.append(note)
    del data[key]


def edit(key):
    now = datetime.now().timestamp()
    data = container.Data()
    versions = container.Versions()
    note = data[key]
    versions.append(note)
    note.updated = now
    note.revision += 1
    tmp_file = helper.create_tempfile()

    with open(tmp_file, 'w') as f:
        f.write(note.content)

    subprocess.call([config.EDITOR, tmp_file])

    with open(tmp_file, 'r') as f:
        note.content = f.read()

    data[key] = note
    os.remove(tmp_file)


def compare(key, to_rev, from_rev):
    data = container.Data()
    versions = container.Versions()

    if data[key].revision == to_rev:
        to_note = data[key]
    else:
        for n in versions:
            if n.uuid == data[key].uuid and n.revision == to_rev:
                to_note = n

    for n in versions:
        if n.uuid == to_note.uuid and n.revision == from_rev:
            from_note = n

    from_content = from_note.content.splitlines()
    to_content = to_note.content.splitlines()
    from_date = datetime.fromtimestamp(from_note.updated)
    from_date = from_date.strftime(config.DATEFORMAT)
    to_date = datetime.fromtimestamp(to_note.updated)
    to_date = to_date.strftime(config.DATEFORMAT)
    from_title = from_note.title + ', revision: ' + str(from_note.revision)
    to_title = to_note.title + ', revision: ' + str(to_note.revision)

    diff = difflib.unified_diff(from_content, to_content,
                                fromfile=from_title,
                                tofile=to_title,
                                fromfiledate=from_date,
                                tofiledate=to_date)

    for line in diff:
        print(line)


def list():
    table = report.DataTable()

    if table:
        print(table)
    else:
        print('You have no data in pynote. :-)')
