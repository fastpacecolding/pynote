import os
import os.path
import argparse
import configparser

from pynote import config


def create_config_string():
    """
    Just create a new config string and let
    the user know what to put in his ~/.noterc.

    """
    config_dict = collect_data()
    print(_("Write this to your '~/.noterc':"))
    print_config(config_dict)


def create_noterc(force=False):
    """
    Create a ~/.noterc and initialize the data_dir
    directory.  If files already exist skip.

    args:
        - force:        Overwrite an existing noterc.

    """
    config_dict = collect_data()
    config_parser = configparser.ConfigParser()
    config_parser['DEFAULT'] = config_dict

    if not os.path.exists(config.NOTERC) or force:
        with open(config.NOTERC, 'w') as f:
            config_parser.write(f)

        # Show some information about the created config.
        print()
        print(_("The following config has been written to '~/.noterc':"))
        print_config(config_dict)
    else:
        print(_("A '~/.noterc' already exists, use '--force' to overwrite!"))

    if not os.path.exists(config_dict['data']):
        os.makedirs(config_dict['data'])
        init_data(config_dict['data'])
    else:
        print()
        print(_("Directory '{}' already exists!").format(config_dict['data']))
        print(_('Choose another directory or delete it manually!'))


def collect_data():
    """
    Ask the user about his prefered settings.
    Returns a dict with the entered values.

    """
    # Ask where to store data.
    print(_('Where do you want to store your notes?'))
    data_dir = input('[default: ~/.note] ')
    data_dir = data_dir or '~/.note'
    data_dir = os.path.expanduser(data_dir)
    print()

    # Ask dateformat.
    print(_('Enter your prefered dateformat!'))
    dateformat = input('[default: Y-m-d H:M] ')
    dateformat = dateformat or 'Y-m-d H:M'
    print()

    # Choose editor.
    editor_env = os.getenv('EDITOR', default='nano')
    print(_('What is your prefered editor?'))
    editor_user = input('[default: {}] '.format(editor_env))
    editor = editor_user or editor_env
    print()

    # Choose pygments theme.
    print(_('Which pygments theme do you like?'))
    print(_('If you have no idea you can have a look in the wiki!'))
    print(_('http://redmine.sevenbyte.org/projects/pynote/wiki/Configuration'))
    pygments_theme = input('[default: default] ')
    pygments_theme = pygments_theme or 'default'
    print()

    config_dict = {'data': data_dir,
                   'dateformat': dateformat,
                   'editor': editor,
                   'pygments_theme': pygments_theme}

    return config_dict


def init_data(data_dir):
    data = os.path.join(data_dir, 'data.json')
    trash = os.path.join(data_dir, 'trash.json')
    revisions = os.path.join(data_dir, 'revisions.json')

    with open(data, 'w') as d, open(trash, 'w') as t, open(revisions, 'w') as r:
        d.write('[]')
        t.write('[]')
        r.write('[]')


def print_config(config_dict):
    print('[DEFAULT]')
    for key, value in sorted(config_dict.items()):
        print(key, '=', value)
