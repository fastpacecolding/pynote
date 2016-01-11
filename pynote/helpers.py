import click
from . import config


def load_notes(path=config.DATA_PATH):
    """
    Scans the given path and returns a list of notes
    which is sorted by the modification time. Any directory
    and the tagfile is ignored. Die path argument has to be
    an instance of pathlib.Path.
    """
    # Circular dependency...
    from . import Note
    if path.exists():
        data = [Note(f) for f in path.iterdir()
                if f.is_file() and f.suffix not in config.IGNORE_EXTENSIONS]
        return sorted(data, key=lambda n: n.age)
    else:
        # TODO: Clean that stuff up here. Do not exit after creating DATA_PATH
        error('The directory {} does not exist!'.format(path))
        echo('Creating new directory {}.'.format(path))
        path = config.DATA_PATH
        path.mkdir(parents=True)
        exit(1)


def get_note(data, key):
    """A wrapper for getting a note out of a list of notes."""
    if key < len(data):
        note = data[key]
        return note
    else:
        die('This note does not exist!')


def echo(text, no_pager=False):
    """A helper which decides between using a pager or not."""
    if click.get_terminal_size()[1] < len(text.splitlines()) and not no_pager:
        click.echo_via_pager(text)
    else:
        click.echo(text)


def info(text):
    """Add 'Info: ' prefix and colorize output."""
    msg = 'Info: ' + text
    if config.COLORS:
        click.secho(msg, fg='yellow')
    else:
        click.echo(msg)


def error(text):
    """Add 'Error: ' prefix and colorize output."""
    msg = 'Error: ' + text
    if config.COLORS:
        click.secho(msg, fg='red')
    else:
        click.echo(msg)


def die(text):
    """A shortcut for error(); die()."""
    error(text)
    exit(1)
