# REFACTOR: This module needs to be refactored!
#   Ugly code stays here until the next minor release as a quick
#   and dirty fix for #365.

import os.path
import configparser

from pynote import helper


noterc = os.path.expanduser('~/.noterc')

# Set default values, see #365.
DATA = os.path.expanduser('~/.note')
DATA_FILE = os.path.join(DATA, 'data.json')
TRASH_FILE = os.path.join(DATA, 'trash.json')
REVISIONS_FILE = os.path.join(DATA, 'revisions.json')
DATEFORMAT = '%Y-%m-%d %H:%M'
PYGMENTS_THEME = 'default'

# Check if noterc exists, see #365.
if os.path.exists(noterc):
    config = configparser.ConfigParser()
    config.read()

    if 'data' in config['DEFAULT']:
        DATA = os.path.expanduser(config['DEFAULT']['data'])

    if 'dateformat' in config['DEFAULT']:
        DATEFORMAT = helper.expand_dateformat(config['DEFAULT']['dateformat'])

    if 'pygments_theme' in config['DEFAULT']:
        PYGMENTS_THEME = config['DEFAULT']['pygments_theme']

    if config['DEFAULT']['editor']:
        EDITOR = config['DEFAULT']['editor']
    elif os.getenv('EDITOR'):
        EDITOR = os.getenv('EDITOR')
