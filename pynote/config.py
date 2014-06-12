import os.path
import configparser
import json


NOTERC = os.path.expanduser('~/.noterc')
CONFIG = configparser.ConfigParser()
CONFIG.read(NOTERC)


DATA = CONFIG.get('DEFAULT', 'data', fallback='~/.note')
DATA = os.path.expanduser(DATA)

EDITOR = CONFIG.get('DEFAULT', 'editor', fallback=os.getenv('EDITOR', 'nano'))
DATEFORMAT = CONFIG.get('DEFAULT', 'dateformat', fallback='YYYY-MM-dd HH:mm')
LOCALE = CONFIG.get('DEFAULT', 'locale', fallback='en_US')
RELDATES = CONFIG.getboolean('DEFAULT', 'reldates', fallback=False)
PYGMENTS_THEME = CONFIG.get('DEFAULT', 'pygments_theme', fallback='default')

IGNORE_SUFFIXES = CONFIG.get('DEFAULT', 'ignore_suffixes', fallback=[])
IGNORE_SUFFIXES = json.loads(IGNORE_SUFFIXES) if IGNORE_SUFFIXES else []
