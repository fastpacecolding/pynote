import os.path
import configparser


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.noterc'))

try:
    DATA_FILE = os.path.expanduser(config['paths']['data'])
    TRASH_FILE = os.path.expanduser(config['paths']['trash'])
    VERSIONS_FILE = os.path.expanduser(config['paths']['versions'])

    if config['misc']['editor']:
        EDITOR = config['misc']['editor']
    elif os.getenv('EDITOR'):
        EDITOR = os.getenv('EDITOR')
    else:
        EDITOR = 'nano'
except KeyError as exception:
    print("It's something wrong with your 'noterc' in the {0} section.".format(exception))
    print("Try running 'note-init' to create a valid 'noterc'!")
    exit()
