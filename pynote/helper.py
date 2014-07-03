import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
from pygments.util import ClassNotFound
from pygments.styles import get_all_styles


def get_note(data, key):
    try:
        note = data[key]
    except IndexError:
        print('Error: This note does not exist!')
        exit(1)
    return note


def highlight(data, lang):
    # Avoid circular importing.
    from pynote import config

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
