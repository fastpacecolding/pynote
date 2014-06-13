import shlex
import subprocess

from plaintable import Table

from pynote import config
from pynote import helper
from pynote import container


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
    data = container.load_notes()
    notes = []

    for i, note in enumerate(data):
        if config.RELDATES:
            header = ['ID', 'Title', 'Age']
            notes.append([i, note.title, note.format_age()])
        else:
            header = ['ID', 'Title', 'Updated']
            notes.append([i, note.title, note.format_updated()])

    print(Table(notes, headline=header))


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
    data = container.load_notes()
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
    data = container.load_notes()

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


# ----------------------------------------
# - Stuff for deleting and editing notes -
# ----------------------------------------

def new(title):
    """
    Create a new note and save it in data.json.

    """
    try:
        note = container.Note.create(title)
    except FileExistsError:
        print('Error: This note already exists!')
        exit(1)

    cmd = shlex.split(config.EDITOR) + [str(note.path)]
    subprocess.call(cmd)


def edit(key):
    """
    Edit a note's content or title and create new revision.

    """
    notes = container.load_notes()
    try:
        note = notes[key]
    except IndexError:
        helper.exit_not_exists()

    cmd = shlex.split(config.EDITOR) + [str(note.path)]
    subprocess.call(cmd)
