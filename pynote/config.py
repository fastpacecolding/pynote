import json
import os
import os.path
import configparser
from xdg import BaseDirectory
from pathlib import Path


global_config = Path('/etc//xdg/noterc')

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
    data_path = Path(_xdg_data)
else:
    data_path = Path(os.path.expanduser('~/.note'))

# Initialize config parser object
# Read global config first, overwrite with local config
config = configparser.ConfigParser()
config.read([str(global_config), str(local_config)])

# fix #14
if 'data' not in config.sections():
    config.add_section('data')
if 'ui' not in config.sections():
    config.add_section('ui')

# data section
# Overwrite data and trash path when it is set in .noterc.
if 'data_path' in config['data']:
    data_path = config.get('data', 'data_path')
    data_path = Path(os.path.expanduser(data_path))
trash_path = data_path / '.trash'
if 'trash_path' in config['data']:
    trash_path = config.get('data', 'trash_path')
    trash_path = Path(os.path.expanduser(trash_path))
extension = config.get('data', 'extension', fallback='')
ignore_extensions = config.get('data', 'ignore_extensions', fallback=[])
ignore_extensions = json.loads(ignore_extensions) if ignore_extensions else []
no_tempfile = config.get('data', 'no_tempfile', fallback=False)

# user interface (ui) section
editor = config.get('ui', 'editor', fallback=os.getenv('EDITOR', 'nano'))
colors = config.getboolean('ui', 'colors', fallback=False)
dateformat = config.get('ui', 'dateformat', fallback='YYYY-MM-dd HH:mm')
reldates = config.getboolean('ui', 'reldates', fallback=False)
locale = config.get('ui', 'locale', fallback='en_US')
pygments_theme = config.get('ui', 'pygments_theme', fallback='default')
