import hashlib
import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
from pygments.util import ClassNotFound
from pygments.styles import get_all_styles
from tempfile import NamedTemporaryFile


def exit_not_exists():
    print('Error: This note does not exist!')
    exit(1)


def highlight(data, lang):
    from pynote import config  # avoid circular importing

    try:
        lexer = lexers.get_lexer_by_name(lang)
    except ClassNotFound:
        print('Lexer not found!')
        exit(1)

    try:
        formatter = formatters.Terminal256Formatter(style=config.PYGMENTS_THEME)
    except ClassNotFound:
        styles = list(get_all_styles())
        print('Theme {} not found!'.format(config.PYGMENTS_THEME))
        print("Please correct pygments_theme in your '~/.noterc'!")
        print('Supported themes are:')
        print()
        for style in styles:
            print(style)
        exit(1)

    data = pygments.highlight(data, lexer, formatter)
    return data


# DEPRECATED
def get_md5(item):
    return hashlib.md5(item.encode('UTF-8')).digest()

def get_sha512(item):
    return hashlib.sha512(item.encode('UTF-8')).digest()
