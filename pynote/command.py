import os
import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile
import difflib
import hashlib

from pynote import config
from pynote import container
from pynote import helper
from pynote import report


def new(title):
    """
    Create a new note and save it in data.json and versions.json.

    """
    data = container.Data()
    versions = container.Versions()
    note = container.Note.create(title)
    tmp_file = helper.create_tempfile()

    # Open the chosen editor to enter the content.
    # Read the entered data from the tempfile.
    subprocess.call([config.EDITOR, tmp_file])
    with open(tmp_file, 'r') as f:
        note.content = f.read()

    data.append(note)
    versions.append(note)
    os.remove(tmp_file)  # Clean tempfile.


def show(key, no_header):
    """
    Show a specific note.  If no_header is true only the
    Note.__str__() method is used.

    """
    data = container.Data()
    note = data[key]

    if no_header:
        print(note)
    else:
        print(note.header())
        print(note)


def delete(key):
    """
    Remove a note from data.json, increment the
    revision number and append it to versions.json
    and trash.json.

    """
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
    """
    Edit a note's content and create new revisions.

    """
    now = datetime.now().timestamp()
    data = container.Data()
    versions = container.Versions()
    note = data[key]
    # Create the content's MD5sum to detect changes.
    # String has to be converted to bytes before passing
    # it to hashlib.md5().
    md5_old = hashlib.md5(note.content.encode('UTF-8')).digest()

    # At first append the old revision
    # to versions.json and increment
    # the revision number.
    versions.append(note)
    note.updated = now
    note.revision += 1
    tmp_file = helper.create_tempfile()

    with open(tmp_file, 'w') as f:
        f.write(note.content)

    subprocess.call([config.EDITOR, tmp_file])

    with open(tmp_file, 'r') as f:
        note.content = f.read()

    md5_new = hashlib.md5(note.content.encode('UTF-8')).digest()

    # Check if there are changes. Otherwise
    # do not create a new revision.
    if md5_old != md5_new:
        data[key] = note
        # Also append the updated note to
        # versions.json, see #276.
        versions.append(note)
    else:
        print('You have not changed anything!')
        print('No new revision has been created!')

    os.remove(tmp_file)  # Clean tempfile.


def compare(key, to_rev, from_rev):
    """
    Compare the given revisions of a note and create a unified diff.

    """
    data = container.Data()
    versions = container.Versions()
    note = data[key]
    to_note, from_note = None, None

    for v in versions:
        if v.uuid == note.uuid and v.revision == to_rev:
            to_note = v
        if v.uuid == note.uuid and v.revision == from_rev:
            from_note = v

    # Check if both versions have been found.  Otherwise
    # let the user know there are no revisions.
    if to_note and from_note:
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
    else:
        print('An error occured. Maybe the revisions do not exist.')


def list():
    """
    Print out a table with all notes.

    """
    table = report.DataTable()

    if table:
        print(table)
    else:
        print('You have no data in pynote. :-)')
