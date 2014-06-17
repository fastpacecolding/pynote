import os.path
import configparser
import json


GLOBAL_NOTERC = '/etc/noterc'
NOTERC = os.path.expanduser('~/.noterc')
CONFIG = configparser.ConfigParser()
CONFIG.read(GLOBAL_NOTERC)
CONFIG.read(NOTERC)


DATA = CONFIG.get('DEFAULT', 'data', fallback='~/.note')
DATA = os.path.expanduser(DATA)

EDITOR = CONFIG.get('DEFAULT', 'editor', fallback=os.getenv('EDITOR', 'nano'))
DATEFORMAT = CONFIG.get('DEFAULT', 'dateformat', fallback='YYYY-MM-dd HH:mm')
LOCALE = CONFIG.get('DEFAULT', 'locale', fallback='en_US')
RELDATES = CONFIG.getboolean('DEFAULT', 'reldates', fallback=False)
PYGMENTS_THEME = CONFIG.get('DEFAULT', 'pygments_theme', fallback='default')
EXTENSION = CONFIG.get('DEFAULT', 'extension', fallback=None)

IGNORE_EXTENSION = CONFIG.get('DEFAULT', 'ignore_extension', fallback=[])
IGNORE_EXTENSION = json.loads(IGNORE_EXTENSION) if IGNORE_EXTENSION else []
