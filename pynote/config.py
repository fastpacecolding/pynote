import os.path
import configparser

from pynote import helper


NOTERC = os.path.expanduser('~/.noterc.devel')
config = configparser.ConfigParser()
config.read(NOTERC)


DATA = config.get('DEFAULT', 'data', fallback='~/.note')
DATA = os.path.expanduser(DATA)

DATA_FILE = os.path.join(DATA, 'data.json')
TRASH_FILE = os.path.join(DATA, 'trash.json')
REVISIONS_FILE = os.path.join(DATA, 'revisions.json')

DATEFORMAT = config.get('DEFAULT', 'dateformat', fallback='Y-m-d H:M')
DATEFORMAT = helper.expand_dateformat(DATEFORMAT)

PYGMENTS_THEME = config.get('DEFAULT', 'pygments_theme', fallback='default')
EDITOR = config.get('DEFAULT', 'editor', fallback=os.getenv('EDITOR', 'nano'))
