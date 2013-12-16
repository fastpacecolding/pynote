import os.path
import configparser


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.noterc'))

try:
    DATA_FILE = os.path.expanduser(config['DEFAULT']['data'])
    TRASH_FILE = os.path.expanduser(config['DEFAULT']['trash'])
    VERSIONS_FILE = os.path.expanduser(config['DEFAULT']['versions'])

    if config['DEFAULT']['editor']:
        EDITOR = config['DEFAULT']['editor']
    elif os.getenv('EDITOR'):
        EDITOR = os.getenv('EDITOR')
    else:
        EDITOR = 'nano'
except KeyError as exception:
    print("It's something wrong with your 'noterc' in the {0} section.".format(exception))
    print("Try running 'note-init' to create a valid 'noterc'!")
    exit()
