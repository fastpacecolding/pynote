import os
import os.path
import argparse
import configparser

import pynote


def run(config=False, force=False):
    noterc = os.path.expanduser('~/.noterc')

    # Ask where to store data.
    print(_('Where do you want to store your notes [default: ~/.note]?'))
    data_dir = input('--> ')
    data_dir = data_dir if data_dir != '' else '~/.note'
    data_dir = os.path.expanduser(data_dir)

    # Ask dateformat.
    print(_('Enter your prefered dateformat [default: Y-m-d H:M]!'))
    dateformat = input('--> ')
    dateformat = dateformat if dateformat != '' else 'Y-m-d H:M'

    # Choose editor.
    editor_env = os.getenv('EDITOR', default='nano')
    print(_('What is your prefered editor [default: {}]?').format(editor_env))
    editor_user = input('--> ')
    editor = editor_user if editor_user != '' else editor_env

    config_dict = {'data': data_dir,
                   'dateformat': dateformat,
                   'editor': editor}

    if config:
        print_config(config_dict)
    else:
        config = configparser.ConfigParser()
        config['DEFAULT'] = config_dict

        if not os.path.exists(noterc) or force:
            with open(noterc, 'w') as f:
                config.write(f)

            # Show some information about the created config.
            print()
            print(_("The following config has been written to '~/.noterc':"))
            print()
            print
        else:
            print(_("A '~/.noterc' already exists, use '--force' to overwrite!"))

        if not os.path.exists(data_dir):
            os.mkdirs(notedir)
            init_data(data_dir)
        else:
            print(_("Directory '{}' already exists!").format(data_dir))


def init_data(data_dir):
    data = os.path.join(data_dir, 'data.json')
    trash = os.path.join(data_dir, 'trash.json')
    revisions = os.path.join(data_dir, 'revisions.json')

    with open(data, 'w') as f:
        f.write('[]')
    with open(trash, 'w') as f:
        f.write('[]')
    with open(revisions, 'w') as f:
        f.write('[]')


def print_config(config_dict):
    print('\r')
    print(_("Write this to your '~/.noterc':"))
    for item in config_dict.items():
        print(item[0], '=', item[1])


if __name__ == '__main__':
    run()
