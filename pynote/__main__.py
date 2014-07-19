from pathlib import Path
import click
from plaintable import Table
import pynote
from pynote import config
from pynote import crypt
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
@click.option('--no-pager', is_flag=True, help="Supress paging long output.")
@click.option('--no-header', is_flag=True, help="Supress header.")
@pass_ctx
def cli(ctx, no_pager, no_header):
    ctx.data = load_notes()
    ctx.no_pager = no_pager
    ctx.no_header = no_header


@cli.command()
@pass_ctx
def list(ctx):
    """Print out a table with all notes."""
    notes = []

    for i, note in enumerate(ctx.data):
        if config.reldates:
            header = ['ID', 'Title', 'Age']
            notes.append([i, note.title, note.format_age()])
        else:
            header = ['ID', 'Title', 'Updated']
            notes.append([i, note.title, note.format_updated()])

    echo(str(Table(notes, headline=header)))


@cli.command()
@click.argument('key', type=int)
@click.option('-l', '--lang', default=None)
@pass_ctx
def show(ctx, key, lang):
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
@click.option('-t', '--title', is_flag=True)
@pass_ctx
def edit(ctx, key, title):
    """Edit a specific note."""
    note = get_note(ctx.data, key)
    if title:
        new_title = click.edit(note.title, editor=config.editor)
        if new_title:
            new_title = new_title.strip()
        else:
            echo_hint('No changes detected')

        new_path = note.path.parent / Path(new_title)
        note.path.rename(new_path)
        note.path = new_path
        note.path.touch()  # Update mtime
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
    note.content = content.encode() if content else ''


@cli.command()
@click.argument('key', type=int)
@click.password_option()
@pass_ctx
def encrypt(ctx, key, password):
    note = get_note(ctx.data, key)

    aes_key = crypt.password_digest(password)
    ciphertext = crypt.encrypt(note.content, aes_key)
    encrypted_note = Note.create(note.title, encrypted=True)

    # TODO: Refacator this out, see container.Note
    with encrypted_note.path.open('bw') as f:
        f.write(ciphertext)


@cli.command()
@click.argument('key', type=int)
@click.password_option()
@pass_ctx
def decrypt(ctx, key, password):
    note = get_note(ctx.data, key)

    aes_key = crypt.password_digest(password)
    ciphertext = crypt.encrypt(note.content, aes_key)
    print(ciphertext)


if __name__ == '__main__':
    cli()
