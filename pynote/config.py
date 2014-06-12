import os.path
import configparser


NOTERC = os.path.expanduser('~/.noterc')
CONFIG = configparser.ConfigParser()
CONFIG.read(NOTERC)


DATA = CONFIG.get('DEFAULT', 'data', fallback='~/.note')
DATA = os.path.expanduser(DATA)

DATA_FILE = os.path.join(DATA, 'data.json')
TRASH_FILE = os.path.join(DATA, 'trash.json')
REVISIONS_FILE = os.path.join(DATA, 'revisions.json')

DATEFORMAT = CONFIG.get('DEFAULT', 'dateformat', fallback='YYYY-MM-dd HH:mm')
LOCALE = CONFIG.get('DEFAULT', 'locale', fallback='en_US')
RELDATES = CONFIG.getboolean('DEFAULT', 'reldates', fallback=False)

PYGMENTS_THEME = CONFIG.get('DEFAULT', 'pygments_theme', fallback='default')
EDITOR = CONFIG.get('DEFAULT', 'editor', fallback=os.getenv('EDITOR', 'nano'))
