import os
import sys
import difflib
import hashlib
import subprocess
from datetime import datetime

from pynote import config
from pynote import container
from pynote import helper
from pynote import report


# FIXME: Conflict with python builtin list() function.
def list():
    """
    Print out a table with all notes.

    """
    table = report.DataTable()

    if table:
        print(table)
    else:
        print(_('You have no data in pynote... :-)'))


def show(key, no_header=False, lang=None):
    """
    Show a specific note.

    args:
        - key:          numeric key of the note in the
                        data container
        - no_header:    supress the note header
        - lang:         specify a programming language
                        for pygments highlighting

    """
    data = container.Data()
    try:
        note = data[key]
    except IndexError:
        helper.exit_not_exists()

    # Send note.content to pygments if lang is not None.
    content = helper.highlight(note.content, lang) if lang else note.content

    if no_header:
        print(content, end='')
    else:
        print(note.header(), end='')
        print(content, end='')


def new(title):
    """
    Create a new note and save it in data.json.

    """
    data = container.Data()
    note = container.Note.create(title)
    tmp_file = helper.create_tempfile()

    # Open the chosen editor to enter the content.
    # Read the entered data from the tempfile.
    subprocess.call([config.EDITOR, tmp_file])
    with open(tmp_file, 'r') as f:
        note.content = f.read()

    data.append(note)
    os.remove(tmp_file)  # Clean tempfile.


def edit(key):
    """
    Edit a note's content and create new revisions.

    """
    now = datetime.now()
    data = container.Data()
    revisions = container.Revisions()
    try:
        note = data[key]
    except IndexError:
        helper.exit_not_exists()
    # Create the content's MD5sum to detect any changes.
    # String has to be converted to bytes before passing
    # it to hashlib.md5().
    md5_old = hashlib.md5(note.content.encode('UTF-8')).digest()

    # At first append the old revision
    # to revisions.json and increment
    # the revision number.
    revisions.append(note)
    note.updated = now
    note.revision += 1
    tmp_file = helper.create_tempfile()

    with open(tmp_file, 'w') as f:
        f.write(note.content)

    subprocess.call([config.EDITOR, tmp_file])

    with open(tmp_file, 'r') as f:
        note.content = f.read()

    md5_new = hashlib.md5(note.content.encode('UTF-8')).digest()

    # Check if there are any changes.
    # Otherwise do not create a new revision.
    if md5_old != md5_new:
        data[key] = note
    else:
        print(_('You have not changed anything!'))
        print(_('No new revision has been created!'))

    os.remove(tmp_file)  # Clean tempfile.


def delete(key):
    """
    Remove a note from data.json, increment the
    revision number and append it to trash.json.

    """
    now = datetime.now()
    data = container.Data()
    trash = container.Trash()
    try:
        note = data[key]
    except IndexError:
        helper.exit_not_exists()
    note.deleted = now

    # Just move the note from trash to data.
    # Do not create a new revision because
    # a deleted note has a deletion time.
    trash.append(note)
    del data[key]


def trash():
    """
    Print out a table with all notes in trash.

    """
    table = report.TrashTable()

    if table:
        print(table)
    else:
        print(_('You have no data in pynote trash... :-)'))


def restore(key):
    """
    Restore a note from trash.

    """
    now = datetime.now()
    data = container.Data()
    trash = container.Trash()
    try:
        note = trash[key]
    except IndexError:
        helper.exit_not_exists()
    note.deleted = None

    # Just move the note from trash to data.
    # Do not create a new revision because
    # a deleted note has a deletion time.
    data.append(note)
    del trash[key]


def compare(key, to_rev, from_rev):
    """
    Compare the given revisions of a note and create a unified diff.

    """
    data = container.Data()
    revisions = container.Revisions()
    note = data[key]
    uuid = note.uuid
    from_note = None
    to_note = note if note.revision == to_rev else None

    for v in revisions:
        # If to_rev is the most recent revision in data then it has
        # already been set.
        if to_note is None and (v.uuid == uuid and v.revision == to_rev):
            to_note = v
        if v.uuid == uuid and v.revision == from_rev:
            from_note = v

    # Check if both revisions have been found.  Otherwise
    # let the user know there are no revisions.
    # splitlines(keepends=True) ensures '\n' endings.
    if to_note and from_note:
        from_content = from_note.content.splitlines(keepends=True)
        to_content = to_note.content.splitlines(keepends=True)
        from_date = from_note.updated.strftime(config.DATEFORMAT)
        to_date = to_note.updated.strftime(config.DATEFORMAT)
        from_title = from_note.title + ', revision: ' + str(from_note.revision)
        to_title = to_note.title + ', revision: ' + str(to_note.revision)

        diff = difflib.unified_diff(from_content, to_content,
                                    fromfile=from_title,
                                    tofile=to_title,
                                    fromfiledate=from_date,
                                    tofiledate=to_date)

        diff = ''.join(tuple(diff))
        diff = helper.highlight(diff, lang='diff')
        print(diff, end='')
    else:
        print(_('Error: Maybe the revisions do not exist?'))
