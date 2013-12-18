import argparse

import pynote
import pynote.command as note
from pynote.report import DataTable
from pynote.report import TrashTable


def run():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest='cmd')

    parser_add = subparser.add_parser('list', help='Show a table with all notes.')
    parser_add = subparser.add_parser('trash', help='Show a table with all deleted notes.')

    parser_add = subparser.add_parser('new', help='Create a new note.')
    parser_add.add_argument('title', type=str)

    parser_add = subparser.add_parser('show', help='Show a specific note.')
    parser_add.add_argument('key', type=int, help='The integer ID which is shown in the table.')

    parser_delete = subparser.add_parser('delete', help='Move a note to trash.')
    parser_delete.add_argument('key', type=int, help='The integer ID which is shown in the table.')

    parser_delete = subparser.add_parser('edit', help='Edit a note.')
    parser_delete.add_argument('key', type=int, help='The integer ID which is shown in the table.')

    parser_delete = subparser.add_parser('compare', help='Compare two notes')
    parser_delete.add_argument('key', type=int, help='The integer ID which is shown in the table.')
    parser_delete.add_argument('to_rev', type=int)
    parser_delete.add_argument('from_rev', type=int)

    parser.add_argument('--version', help='Show version.', action='version',
                        version='pynote {0}'.format(pynote.__version__))

    args = parser.parse_args()


    if args.cmd == 'list':
        print(DataTable())
    elif args.cmd == 'new':
        note.new(args.title)
    elif args.cmd == 'delete':
        note.delete(args.key)
    elif args.cmd == 'show':
        note.show(args.key)
    elif args.cmd == 'edit':
        note.edit(args.key)
    elif args.cmd == 'trash':
        print(TrashTable())
    elif args.cmd == 'compare':
        if args.to_rev > args.from_rev:
            note.compare(args.key, args.to_rev, args.from_rev)
        else:
            print('Error: from_rev must not be smaller than to_rev!')
            exit(1)
