import os.path
import configparser

from pynote import helper


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.noterc'))

try:
    DATA_FILE = os.path.expanduser(config['DEFAULT']['data'])
    TRASH_FILE = os.path.expanduser(config['DEFAULT']['trash'])
    VERSIONS_FILE = os.path.expanduser(config['DEFAULT']['versions'])
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
