import os
import os.path
import argparse
import configparser

import pynote


# TODO:
#  - be interactive, ask the user
#  - implement --force in data dir stuff...


def run():
    # at first parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Remove existing files and re-init pynote.')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    noterc_path = os.path.expanduser('~/.noterc')
    data_dir = os.path.expanduser('~/.note')
    editor = os.getenv('EDITOR', default='nano')
    config['DEFAULT'] = {'data': '~/.note',
                         'dateformat': 'Y-m-d H:M',
                         'editor': editor}

    if not os.path.exists(noterc_path) or args.force:
        with open(noterc_path, 'w') as f:
            config.write(f)
    else:
        print("File '~/.noterc' already exists, use '--force' to overwrite!")

    if not os.path.exists(data_dir):
        os.mkdir(notedir)

        with open(os.path.join(notedir, 'data.json'), 'w') as f:
            f.write('[]')
        with open(os.path.join(notedir, 'trash.json'), 'w') as f:
            f.write('[]')
        with open(os.path.join(notedir, 'revisions.json'), 'w') as f:
            f.write('[]')
    else:
        print("Directory '~/.note' already exists, use '--force' to overwrite!")


if __name__ == '__main__':
    run()
