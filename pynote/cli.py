import textwrap
from pathlib import Path
import click
from plaintable import Table
from . import config, __version__
from .helpers import echo, info, die
from .container import Note, load_notes, get_note


class Context:

    def __init__(self, data=None, no_pager=False):
        self.data = data
        self.no_pager = no_pager

pass_ctx = click.make_pass_decorator(Context, ensure=True)


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))


@click.command(cls=AliasedGroup)
@click.version_option(version=__version__, prog_name='pynote')
@click.option('--no-pager', is_flag=True, help='Supress paging long output.')
@click.option('--no-header', is_flag=True, help='Supress header.')
@pass_ctx
def cli(ctx, no_pager, no_header):
    ctx.data = load_notes()
    ctx.no_pager = no_pager
    ctx.no_header = no_header


@cli.command(name='list')
@pass_ctx
def list_(ctx):
    """Print out a table with all notes."""
    notes = []
    data = enumerate(ctx.data)
    for i, note in data:
        if config.RELDATES:
            header = ['ID', 'Title', 'Age']
            notes.append([i, note.title, note.format_age()])
        else:
            header = ['ID', 'Title', 'Updated']
            notes.append([i, note.title, note.format_updated()])
    # Error handling
    if notes:
        echo(str(Table(notes, headline=header)))
    else:
        die('No notes exist! Create new ones with "note new TITLE"!')


@cli.command()
@click.argument('key', type=int)
@click.option('-w', '--wrap-text', is_flag=True,
              help="Wrap output text at 70 chars.")
@pass_ctx
def show(ctx, key, wrap_text):
    """Show a specific note."""
    note = get_note(ctx.data, key)

    if ctx.no_header:
        output = note.content
    else:
        output = note.format_header() + '\n\n' + note.content

    if wrap_text:
        output = textwrap.fill(output, replace_whitespace=False)

    echo(output, ctx.no_pager)


@cli.command()
@pass_ctx
def all(ctx):
    """Print out all notes in the data directory."""
    output = ''
    for i, note in enumerate(ctx.data):
        counter = '-- note {} --'.format(i)
        counter = click.style(counter, bold=True) if config.COLORS else counter

        output += '\n\n'
        output += counter
        output += '\n\n'

        if ctx.no_header:
            output += note.content
        else:
            output += note.format_header()
            output += '\n\n'
            output += note.content

    echo(output, ctx.no_pager)


@cli.command()
@click.argument('key', type=int)
@click.option('--title', is_flag=True, help='Edit the title instead.')
@click.option('--no-tempfile', is_flag=True, help='Edit note file directly.')
@pass_ctx
def edit(ctx, key, title, no_tempfile):
    """Edit a specific note."""
    note = get_note(ctx.data, key)
    if title:
        new_title = click.edit(note.title, editor=config.EDITOR)
        if new_title:
            new_title = new_title.strip()
            new_path = note.path.parent / Path(new_title)
            note.path.rename(new_path)
            note.update_path(new_path)
            # REVIEW: Can we remove this?
            note.path.touch()
        else:
            info('No changes detected')
    else:
        if config.NO_TEMPFILE or no_tempfile:
            new_content = click.edit(
                note.content,
                editor=config.EDITOR,
                extension=config.EXTENSION,
                filename=note.path
            )
        else:
            new_content = click.edit(
                note.content,
                editor=config.EDITOR,
                extension=config.EXTENSION
            )
        if new_content:
            note.content = new_content
        else:
            info('No changes detected')


@cli.command()
@click.argument('title', type=str)
def new(title):
    """Create a new note."""
    if '/' in title:
        die('Slashes in the title are not allowed!')
    try:
        note = Note.create(title)
    except FileExistsError:
        die('This note already exists!')
    content = click.edit(note.content, editor=config.EDITOR)
    note.content = content if content else ''
    info("New note '{}' created!".format(note.title))


@cli.command()
@click.argument('key', type=int)
@pass_ctx
def restore(ctx, key):
    """Restore a note from trash."""
    note = get_note(ctx.trash, key)
    new_path = config.DATA_PATH / note.title
    note.path.rename(new_path)
    note.update_path(new_path)
    note.path.touch()
    info("Note '{}' restored!".format(note.title))


@cli.command()
def conf():
    """Show pynote's configuration (for debugging)."""
    varlist = [
        ['global_config', config.GLOBAL_CONFIG],
        ['local_config', config.LOCAL_CONFIG],
        ['data_path', config.DATA_PATH],
        ['editor', config.EDITOR],
        ['colors', config.COLORS],
        ['dateformat', config.DATEFORMAT],
        ['reldates', config.RELDATES],
        ['locale', config.LOCALE],
        ['extension', config.EXTENSION],
        ['ignore_extensions', config.IGNORE_EXTENSIONS],
        ['no_tempfile', config.NO_TEMPFILE],
    ]
    echo(str(Table(varlist)))
