import os.path
import configparser

from pynote import helper


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.noterc'))

try:
    DATA = os.path.expanduser(config['DEFAULT']['data'])
    DATA_FILE = os.path.join(DATA, 'data.json')
    TRASH_FILE = os.path.join(DATA, 'trash.json')
    REVISIONS_FILE = os.path.join(DATA, 'revisions.json')
    DATEFORMAT = helper.expand_dateformat(config['DEFAULT']['dateformat'])

    if config['DEFAULT']['editor']:
        EDITOR = config['DEFAULT']['editor']
    elif os.getenv('EDITOR'):
        EDITOR = os.getenv('EDITOR')
    else:
        EDITOR = 'nano'

except KeyError as e:
    print("It's something wrong with your 'noterc' in {0}.".format(e))
    print("Try running 'note-init' to create a valid 'noterc'!")
    exit(1)
