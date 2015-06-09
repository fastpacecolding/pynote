import click
from . import config


def echo(text, no_pager=False):
    """A helper which decides between using a pager or not."""
    if click.get_terminal_size()[1] < len(text.splitlines()) and not no_pager:
        click.echo_via_pager(text)
    else:
        click.echo(text)


def echo_error(text):
    """Add 'Error: ' prefix and colorize output."""
    msg = 'Error: ' + text
    if config.COLORS:
        click.secho(msg, fg='red')
    else:
        click.echo(msg)


def echo_info(text):
    """Add 'Info: ' prefix and colorize output."""
    msg = 'Info: ' + text
    if config.COLORS:
        click.secho(msg, fg='yellow')
    else:
        click.echo(msg)


# NOTE: "highlight" conflicts with click
def highlight_(data, lang):
    """A helper function for highlighting data with pygments."""
    try:
        from pygments import highlight
        from pygments.util import ClassNotFound
        from pygments.styles import get_all_styles
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter
    except ImportError:
        echo_error('Pygments is missing')
        click.echo('Syntax highlighting is provided by pygments.')
        click.echo('Please install pygments (http://pygments.org)!')
        exit(1)

    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        echo_error('Lexer not found!')
        exit(1)

    try:
        formatter = Terminal256Formatter(style=config.PYGMENTS_THEME)
    except ClassNotFound:
        styles = get_all_styles()
        msg = 'Pygments theme {} not found!'.format(config.PYGMENTS_THEME)
        echo_error(msg)
        click.echo("Please correct pygments_theme in your '~/.noterc'!")
        click.echo('Supported themes are:')
        click.echo()
        click.echo('\n'.join(styles))
        exit(1)

    return highlight(data, lexer, formatter)
