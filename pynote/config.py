import json
import os
import os.path
import configparser
from xdg import BaseDirectory
from pathlib import Path


global_config = Path('/etc/xdg/noterc')

_xdg_first_config = BaseDirectory.load_first_config('note')
if _xdg_first_config:
    local_config = Path(_xdg_first_config) / 'noterc'
else:
    local_config = Path(os.path.expanduser('~/.noterc'))

_xdg_data = None
# Just take the first one: '$HOME/.local/share/note'
if list(BaseDirectory.load_data_paths('note')):
    _xdg_data = list(BaseDirectory.load_data_paths('note'))[0]

if _xdg_data:
    DATA_PATH = Path(_xdg_data)
else:
    DATA_PATH = Path(os.path.expanduser('~/.note'))

# Initialize config parser object
# Read global config first, overwrite with local config
config = configparser.ConfigParser()
config.read([str(global_config), str(local_config)])

# fix #14
if 'data' not in config.sections():
    config.add_section('data')
if 'ui' not in config.sections():
    config.add_section('ui')

# [data] section
# Overwrite data and trash path when it is set in .noterc.
if 'path' in config['data']:
    DATA_PATH = config.get('data', 'pathpath')
    DATA_PATH = Path(os.path.expanduser(DATA_PATH))
EXTENSION = config.get('data', 'extension', fallback='')
IGNORE_EXTENSIONS = config.get('data', 'ignore_extensions', fallback=[])
IGNORE_EXTENSIONS = json.loads(IGNORE_EXTENSIONS) if IGNORE_EXTENSIONS else []
NO_TEMPFILE = config.get('data', 'no_tempfile', fallback=False)

# [ui] section
EDITOR = config.get('ui', 'editor', fallback=os.getenv('EDITOR', 'nano'))
COLORS = config.getboolean('ui', 'colors', fallback=False)
DATEFORMAT = config.get('ui', 'dateformat', fallback='YYYY-MM-dd HH:mm')
RELDATES = config.getboolean('ui', 'reldates', fallback=False)
LOCALE = config.get('ui', 'locale', fallback='en_US')
