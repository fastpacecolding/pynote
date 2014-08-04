import json
import os
import os.path
import configparser
from pathlib import Path


# Set global and local config paths. Pynote supports XDG Base Directory
# Specification. If the environment variable XDG_CONFIG_HOME is set choose
# $XDG_CONFIG_HOME/note/noterc otherwise fall back to $HOME/.config/note/noterc
# but only if this file exists. If this file is not present always fall back to
# $HOME/.noterc.
global_config = Path('/etc/noterc')
if os.getenv('XDG_CONFIG_HOME'):
    local_config = Path(os.getenv('XDG_CONFIG_HOME')) / Path('note/noterc')
elif Path(os.path.expanduser('~/.config/note/noterc')).exists():
    local_config = Path(os.path.expanduser('~/.config/note/noterc'))
else:
    local_config = Path(os.path.expanduser('~/.noterc'))

# Set pynote's data path according to XDG Base Directory Specification. If
# XDG_DATA_HOME is set choose $XDG_DATA_HOME/note otherwise fall back to
# $HOME/.local/share/note but only if this directory exists. If it does not
# exist fall back to $HOME/.note. This value can also be overwritten in the
# global or local configfile.
if os.getenv('XDG_DATA_HOME'):
    data = Path(os.getenv('XDG_DATA_HOME')) / Path('note')
elif Path(os.path.expanduser('~/.local/share/note')).exists():
    data = Path(os.path.expanduser('~/.local/share/note'))
else:
    data = Path(os.path.expanduser('~/.note'))


# Initialize config parser object
# Read global config first, overwrite with local config
config = configparser.ConfigParser()
config.read([str(global_config), str(local_config)])

# fix #14
if not 'ui' in config.sections():
    config.add_section('ui')
if not 'data' in config.sections():
    config.add_section('data')

# user interface (ui) section
editor = config.get('ui', 'editor', fallback=os.getenv('EDITOR', 'nano'))
colors = config.getboolean('ui', 'colors', fallback=False)
dateformat = config.get('ui', 'dateformat', fallback='YYYY-MM-dd HH:mm')
reldates = config.getboolean('ui', 'reldates', fallback=False)
locale = config.get('ui', 'locale', fallback='en_US')
pygments_theme = config.get('ui', 'pygments_theme', fallback='default')

# data section
data = config.get('data', 'path', fallback='~/.note')
data = os.path.expanduser(data)
extension = config.get('data', 'extension', fallback='')
ignore_extensions = config.get('data', 'ignore_extensions', fallback=[])
ignore_extensions = json.loads(ignore_extensions) if ignore_extensions else []
