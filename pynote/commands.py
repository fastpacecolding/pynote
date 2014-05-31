import os
import sys
import shutil
import difflib
import hashlib
import subprocess
from datetime import datetime
from prettytable import PrettyTable

from plaintable import Table
from pynote import containerng

from pynote import config
from pynote import container
from pynote import helper
from pynote import report


# ---------------------------------------------
# - Commands for reading and displaying notes -
# ---------------------------------------------

def list_(tags=None):
    """
    Print out a table with all notes.

    args:
        - tags:         a tuple with tags which should be
                        filtered , e.g.: ('tag1', 'tag2')

    """
    data = containerng.Notes()
    notes = []

    for i, note in enumerate(data):
        notes.append([i, note.title, note.updated])
    notes = sorted(notes, key=lambda l: l[2], reverse=True)
    print(Table(notes, headline=['ID', 'Title', 'Updated'],
          datetimefs=config.DATEFORMAT))


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
    data = containerng.Notes()
    try:
        note = data[key]
    except IndexError:
        helper.exit_not_exists()

    # Send note.content to pygments if lang is not None.
    content = helper.highlight(note.content, lang) if lang else note.content

    if no_header:
        print(content)
    else:
        print(note.get_header())
        print()
        print(content)


def show_all(no_header=False):
    """
    Print all notes in data container.

    args:
        - no_header:    supress the note header

    """
    data = containerng.Notes()

    for i, note in enumerate(data):
        print()
        print()
        print('-- note {} --'.format(i))
        print()

        if no_header:
            print(note.content)
        else:
            print(note.get_header())
            print()
            print(note.content)


def trash():
    """
    Print out a table with all notes in trash.

    """
    table = report.TrashTable()

    if table:
        print(table)
    else:
        print('You have no data in pynote trash... :-)')


# ----------------------------------------
# - Stuff for deleting and editing notes -
# ----------------------------------------

def new(title):
    """
    Create a new note and save it in data.json.

    """
    try:
        note = containerng.Note.create(title)
    except FileExistsError:
        print('Error: This note already exists!')
        exit(1)

    subprocess.call([config.EDITOR, str(note.path)])


def edit(key):
    """
    Edit a note's content or title and create new revision.

    """
    notes = containerng.Notes()
    try:
        note = notes[key]
    except IndexError:
        helper.exit_not_exists()

    subprocess.call([config.EDITOR, str(note.path)])


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


# --------------------
# - Revision section -
# --------------------

def revisions(key):
    """
    Display the available revisions of a note.

    """
    data = container.Data()
    note = data[key]
    table = report.RevisionsTable(note)

    print("There are {} revisions of '{}':".format(len(table), note.title))
    print()
    print(table)


def compare(key, new_rev, old_rev, color=False):
    """
    Compare the given revisions of a note and create a unified diff.

    """
    data = container.Data()
    revisions = container.Revisions()
    note = data[key]
    uuid = note.uuid
    old_note = None
    new_note = note if note.revision == new_rev else None

    for v in revisions:
        # If new_rev is the most recent revision in data then it has
        # already been set.
        if new_note is None and (v.uuid == uuid and v.revision == new_rev):
            new_note = v
        if v.uuid == uuid and v.revision == old_rev:
            old_note = v

    # Check if both revisions have been found.  Otherwise
    # let the user know there are no revisions.
    # splitlines(keepends=True) ensures '\n' endings.
    if new_note and old_note:
        old_content = old_note.content.splitlines(keepends=True)
        new_content = new_note.content.splitlines(keepends=True)
        old_date = old_note.updated.strftime(config.DATEFORMAT)
        new_date = new_note.updated.strftime(config.DATEFORMAT)
        old_title = old_note.title + ', revision: ' + str(old_note.revision)
        new_title = new_note.title + ', revision: ' + str(new_note.revision)

        diff = difflib.unified_diff(old_content, new_content,
                                    fromfile=old_title,
                                    tofile=new_title,
                                    fromfiledate=old_date,
                                    tofiledate=new_date)

        diff = ''.join(tuple(diff))
        if color is True:
            diff = helper.highlight(diff, lang='diff')
        print(diff)
    else:
        print('Error: Maybe the revisions do not exist?')


# ---------------------
# - Commands for tags -
# ---------------------

def tags():
    """
    Display all available tags.

    """
    data = container.Data()
    tags = set()

    for note in data:
        for tag in note.tags:
            tags.add(tag)
    if tags:
        print('The following tags exist:')
    else:
        print('No tags exist!')

    for tag in tags:
        print(tag)


def note_tags(key):
    """
    Display all available tags of one note.

    """
    data = container.Data()
    note = data[key]
    tags = note.tags

    if tags:
        print('Note {}, {}, is tagged with:'.format(key, note.title))
    else:
        print('Note {}, {}, is not tagged!'.format(key, note.title))

    for tag in tags:
        print(tag)


def add_tags(key, tags=()):
    """
    Add tags to a note.

    """
    data = container.Data()
    note = data[key]
    for tag in tags:
        note.tags.add(tag)

    data[key] = note


def del_tags(key, tags=()):
    """
    Delete tags from a note.

    """
    data = container.Data()
    note = data[key]
    for tag in tags:
        note.tags.discard(tag)

    data[key] = note

