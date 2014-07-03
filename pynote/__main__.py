from pathlib import Path
import click
import pynote
from pynote import config
from pynote import helper
from pynote import crypt
from pynote.container import Note
from pynote.container import load_notes
from pynote.container import get_note
from plaintable import Table


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
@pass_ctx
def cli(ctx, no_pager):
    ctx.data = load_notes()
    ctx.no_pager = no_pager


@cli.command()
@pass_ctx
def list(ctx):
    """Print out a table with all notes."""
    notes = []

    for i, note in enumerate(ctx.data):
        if config.RELDATES:
            header = ['ID', 'Title', 'Age']
            notes.append([i, note.title, note.format_age()])
        else:
            header = ['ID', 'Title', 'Updated']
            notes.append([i, note.title, note.format_updated()])

    click.echo(Table(notes, headline=header))


@cli.command()
@click.argument('key', type=int)
@click.option('-n', '--no-header', is_flag=True)
@pass_ctx
def show(ctx, key, no_header):
    """Show a specific note."""
    note = get_note(ctx.data, key)

    if no_header:
        output = note.content.decode()
    else:
        output = note.get_header() + '\n\n' + note.content.decode()

    condition = (
        click.get_terminal_size()[1] < len(note.content.splitlines())
        and not ctx.no_pager
    )
    if condition:
        click.echo_via_pager(output)
    else:
        click.echo(output)


@cli.command()
@click.option('-n', '--no-header', is_flag=True)
@pass_ctx
def all(ctx, no_header):
    """Print out all notes in the data directory."""
    output = ''
    for i, note in enumerate(ctx.data):
        output += '\n\n'
        output += '-- note {} --'.format(i)
        output += '\n\n'

        if note.is_encrypted:
            output += 'Encrypted note!'
            output += '\n'
        else:
            if no_header:
                output += note.content.decode()
            else:
                output += note.get_header()
                output += '\n\n'
                output += note.content.decode()

    condition = (
        click.get_terminal_size()[1] < len(output.splitlines())
        and not ctx.no_pager
    )
    if condition:
        click.echo_via_pager(output)
    else:
        click.echo(output)


# Maybe obsolete in click 3.0: http://click.pocoo.org/changelog/#version-3-0
@cli.command()
@click.argument('key', type=int)
@click.option('-l', '--lang', default='text')
@click.option('-n', '--no-header', is_flag=True)
@pass_ctx
def highlight(ctx, key, lang, no_header):
    """Show a specific note with synthax highlighting."""
    note = get_note(ctx.data, key)
    output = _highlight(note.content.decode(), lang)
    if no_header is False:
        output = note.get_header() + '\n\n' + output
    click.echo(output)


@cli.command()
@click.argument('key', type=int)
@click.option('-t', '--title', is_flag=True)
@pass_ctx
def edit(ctx, key, title):
    """Edit a specific note."""
    note = get_note(ctx.data, key)
    if title:
        new_title = click.edit(note.title, editor=config.EDITOR)
        new_title = new_title.strip()
        new_path = note.path.parent / Path(new_title)
        note.path.rename(new_path)
        note.path = new_path
        note.path.touch()  # Update mtime
    else:
        click.edit(editor=config.EDITOR, filename=str(note.path))


@cli.command()
@click.argument('title', type=str)
def new(title):
    """Create a new note."""
    try:
        note = Note.create(title)
    except FileExistsError:
        print('Error: This note already exists!')
        exit(1)
    click.edit(editor=config.EDITOR, filename=str(note.path))


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


def _highlight(data, lang):
    """A helper function for highlighting data with pygments."""
    try:
        from pygments import highlight
        from pygments.util import ClassNotFound
        from pygments.styles import get_all_styles
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter
    except ImportError:
        click.secho('Error: Pygments is missing', fg='red')
        click.echo('Syntax highlighting is provided by pygments.')
        click.echo('Please install pygments (http://pygments.org)!')
        exit(1)

    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        click.secho('Error: Lexer not found!', fg='red')
        exit(1)

    try:
        formatter = Terminal256Formatter(style=config.PYGMENTS_THEME)
    except ClassNotFound:
        styles = get_all_styles()
        error_msg = 'Error: Pygments theme {} not found!'.format(config.PYGMENTS_THEME)
        click.secho(error_msg, fg='red')
        click.echo("Please correct pygments_theme in your '~/.noterc'!")
        click.echo('Supported themes are:')
        click.echo()
        click.echo('\n'.join(styles))
        exit(1)

    return highlight(data, lexer, formatter)


if __name__ == '__main__':
    cli()
