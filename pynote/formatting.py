from click import echo
from click import secho
from pynote import config


def echo_error(text):
    if config.COLORS:
        secho(text, fg='red')
    else:
        echo(text)


def highlight(data, lang):
    """A helper function for highlighting data with pygments."""
    try:
        from pygments import highlight
        from pygments.util import ClassNotFound
        from pygments.styles import get_all_styles
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter
    except ImportError:
        secho('Error: Pygments is missing', fg='red')
        echo('Syntax highlighting is provided by pygments.')
        echo('Please install pygments (http://pygments.org)!')
        exit(1)

    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        secho('Error: Lexer not found!', fg='red')
        exit(1)

    try:
        formatter = Terminal256Formatter(style=config.PYGMENTS_THEME)
    except ClassNotFound:
        styles = get_all_styles()
        error_msg = 'Error: Pygments theme {} not found!'.format(config.PYGMENTS_THEME)
        secho(error_msg, fg='red')
        echo("Please correct pygments_theme in your '~/.noterc'!")
        echo('Supported themes are:')
        echo()
        echo('\n'.join(styles))
        exit(1)

    return highlight(data, lexer, formatter)
