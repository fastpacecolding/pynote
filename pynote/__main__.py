import argparse

import pynote
import pynote.command as note


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    # note list
    _list = subparsers.add_parser('list', help='Show a table with all notes.')

    # note show
    show = subparsers.add_parser('show', help='Show a specific note.')
    show.add_argument('key', type=int, help='The integer ID which is shown in the table.')
    show.add_argument('-n', '--no-header', action='store_true', help='Do not show header data.')

    # note new
    new = subparsers.add_parser('new', help='Create a new note.')
    new.add_argument('title', type=str)

    # note edit
    edit = subparsers.add_parser('edit', help='Edit a note.')
    edit.add_argument('key', type=int, help='The integer ID which is shown in the table.')

    # note delete
    delete = subparsers.add_parser('delete', help='Move a note to trash.')
    delete.add_argument('key', type=int, help='The integer ID which is shown in the table.')

    # note trash
    trash = subparsers.add_parser('trash', help='Show a table with all deleted notes.')

    # note restore
    restore = subparsers.add_parser('restore', help='Restore a deleted note.')
    restore.add_argument('key', type=int, help='The integer ID which is shown in the trash table.')

    # note compare
    compare = subparsers.add_parser('compare', help='Compare two notes')
    compare.add_argument('key', type=int, help='The integer ID which is shown in the table.')
    compare.add_argument('to_rev', type=int)
    compare.add_argument('from_rev', type=int)

    # note --version
    parser.add_argument('--version', help='Show version.', action='version',
                        version='pynote {0}'.format(pynote.__version__))

    args = parser.parse_args()

    # Choose the correct function from pynote.command
    # depending on args.cmd.  Choose note list if no
    # command is entered.
    if args.cmd == 'list' or args.cmd is None:
        note.list()
    elif args.cmd == 'show':
        note.show(args.key, args.no_header)
    elif args.cmd == 'new':
        note.new(args.title)
    elif args.cmd == 'edit':
        note.edit(args.key)
    elif args.cmd == 'delete':
        note.delete(args.key)
    elif args.cmd == 'trash':
        note.trash()
    elif args.cmd == 'restore':
        note.restore(args.key)
    elif args.cmd == 'compare':
        if args.to_rev > args.from_rev:
            note.compare(args.key, args.to_rev, args.from_rev)
        else:
            print('Error: from_rev must not be smaller than to_rev!')
            exit(1)


if __name__ == '__main__':
    run()
