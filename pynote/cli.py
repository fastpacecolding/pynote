import textwrap
from pathlib import Path
import click
from plaintable import Table
import pynote
from pynote import config
from pynote.formatting import echo, echo_hint, echo_error, highlight_
from pynote.container import Note, load_notes, get_note, filter_tags


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
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=AliasedGroup)
@click.version_option(version=pynote.__version__, prog_name='pynote')
@click.option('--no-pager', is_flag=True, help='Supress paging long output.')
@click.option('--no-header', is_flag=True, help='Supress header.')
@pass_ctx
def cli(ctx, no_pager, no_header):
    ctx.data = load_notes()
    ctx.trash = load_notes(config.trash_path)
    ctx.no_pager = no_pager
    ctx.no_header = no_header


@cli.command()
@click.option('--trash', is_flag=True, help='Show trash.')
@click.option('-t', '--tags', default=None, help='Filter appropriate tags.')
@click.option('-e', '--extended', is_flag=True, help='Add a tags column.')
@pass_ctx
def list(ctx, trash, tags, extended):
    """Print out a table with all notes."""
    notes = []
    # Choose between data and trash depending on --trash.
    data = enumerate(ctx.data) if not trash else enumerate(ctx.trash)
    data = filter_tags(ctx.data, tags) if tags else data
    for i, note in data:
        if config.reldates:
            if extended:
                header = ['ID', 'Title', 'Age', 'Tags']
                notes.append(
                    [i, note.title, note.format_age(), ', '.join(note.tags)]
                )
            else:
                header = ['ID', 'Title', 'Age']
                notes.append([i, note.title, note.format_age()])
        else:
            if extended:
                header = ['ID', 'Title', 'Updated', 'Tags']
                notes.append(
                    [i, note.title, note.format_age(), ', '.join(note.tags)]
                )
            else:
                header = ['ID', 'Title', 'Updated']
                notes.append([i, note.title, note.format_updated()])
    if notes:
        echo(str(Table(notes, headline=header)))
    else:
        echo_error('No notes exists! Create new ones with "note new TITLE"!')


@cli.command()
@click.argument('key', type=int)
@click.option('-l', '--lang', default=None)
@click.option('-w', '--wrap-text', is_flag=True,
              help="Wrap output text at 70 chars.")
@pass_ctx
def show(ctx, key, lang, wrap_text):
    """Show a specific note."""
    note = get_note(ctx.data, key)
    if lang and config.colors:
        content = highlight_(note.content.decode(), lang)
    elif lang and config.colors is False:
        echo_error('Color support is not enabled!')
        exit(1)
    else:
        content = note.content.decode()

    if ctx.no_header:
        output = content
    else:
        output = note.format_header() + '\n\n' + content

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
        counter = click.style(counter, bold=True) if config.colors else counter

        output += '\n\n'
        output += counter
        output += '\n\n'

        if note.is_encrypted:
            output += 'Encrypted note!'
            output += '\n'
        else:
            if ctx.no_header:
                output += note.content.decode()
            else:
                output += note.format_header()
                output += '\n\n'
                output += note.content.decode()

    echo(output, ctx.no_pager)


@cli.command()
@click.argument('key', type=int)
@click.option('--title', is_flag=True, help='Edit the title instead.')
@click.option('--tags', is_flag=True, help='Edit assigned tags instead.')
@pass_ctx
def edit(ctx, key, title, tags):
    """Edit a specific note."""
    note = get_note(ctx.data, key)
    if title:
        new_title = click.edit(note.title, editor=config.editor)
        if new_title:
            # Delete old tags from tagsfile and save them in a variable.
            tags = note.tags
            del note.tags
            new_title = new_title.strip()
            new_path = note.path.parent / Path(new_title)
            note.path.rename(new_path)
            note.update_path(new_path)
            # Add saved tags to the renamed note.
            # This ensures correct dictionary keys.
            note.tags = tags
            # REVIEW: Can we remove this?
            note.path.touch()
        else:
            echo_hint('No changes detected')
    elif tags:
        tag_str = '# Put each tag in one line! This line will be ignored.\n'
        tag_str += '\n'.join(note.tags)
        new_tags = click.edit(tag_str, editor=config.editor)
        if new_tags:
            new_tags = new_tags.strip().splitlines()
            try:
                note.tags = new_tags[1:]  # strip comment
            except AttributeError:
                echo_error('Tags with spaces are not allowed!')
                exit(1)
        else:
            echo_hint('No changes detected')
    else:
        new_content = click.edit(note.content.decode(), editor=config.editor,
                                 extension=config.extension)
        if new_content:
            note.content = new_content.encode()
        else:
            echo_hint('No changes detected')


@cli.command()
@click.argument('title', type=str)
def new(title):
    """Create a new note."""
    try:
        note = Note.create(title)
    except FileExistsError:
        echo_error('This note already exists!')
        exit(1)
    content = click.edit(note.content.decode(), editor=config.editor)
    note.content = content.encode() if content else b''
    echo_hint("New note '{}' created!".format(note.title))


@cli.command()
@click.argument('key', type=int)
@pass_ctx
def delete(ctx, key):
    """Move a note to trash."""
    # FIXME: Don't loose tags when deleting a note.
    note = get_note(ctx.data, key)
    if not config.trash_path.exists():
        config.trash_path.mkdir()
    new_path = config.trash_path / note.title
    note.path.rename(new_path)
    note.update_path(new_path)
    # REVIEW: Can we remove this?
    note.path.touch()
    echo_hint("Note '{}' moved to trash!".format(note.title))


@cli.command()
@click.argument('key', type=int)
@pass_ctx
def restore(ctx, key):
    """Restore a note from trash."""
    note = get_note(ctx.trash, key)
    new_path = config.data_path / note.title
    note.path.rename(new_path)
    note.update_path(new_path)
    # REVIEW: Can we remove this?
    note.path.touch()
    echo_hint("Note '{}' restored!".format(note.title))
