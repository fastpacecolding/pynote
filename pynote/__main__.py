import argparse

import pynote
import pynote.init
import pynote.commands as note


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    # note list
    list_ = subparsers.add_parser('list', help='show a table with all active notes')
    list_.add_argument('-t', '--tags', nargs='+', help='filter tags')

    # note show
    show = subparsers.add_parser('show', help='show a specific note')
    show.add_argument('key', type=int, nargs='?', default=0,
                      help='integer key which is shown in the table')
    show.add_argument('-a', '--all', action='store_true',
                      help='show all notes')
    show.add_argument('-n', '--no-header', action='store_true',
                      help='do not show header data')
    show.add_argument('-l', '--lang', help='specify synthax highlighting')

    # note new
    new = subparsers.add_parser('new', help='create a new note')
    new.add_argument('title', type=str)

    # note edit
    edit = subparsers.add_parser('edit', help='edit a note')
    edit.add_argument('key', type=int, help='integer key which is shown in the table')
    edit.add_argument('-t', '--title', action='store_true',
                      help='edit the title')

    # note delete
    delete = subparsers.add_parser('delete', help='move a note to trash')
    delete.add_argument('key', type=int, help='integer key which is shown in the table')

    # note trash
    trash = subparsers.add_parser('trash', help='show a table with all deleted notes')

    # note restore
    restore = subparsers.add_parser('restore', help='restore a deleted note')
    restore.add_argument('key', type=int, help='integer key which is shown in the trash table')

    # note compare
    compare = subparsers.add_parser('compare', help='compare two notes')
    compare.add_argument('key', type=int, help='integer key which is shown in the table')
    compare.add_argument('new_rev', type=int, help='new revision number')
    compare.add_argument('old_rev', type=int, help='old revision number')
    compare.add_argument('-c', '--color', action='store_true',
                         help='use colors')

    # DEPRECATED
    # note init
    init = subparsers.add_parser('init', help='initialize pynote')
    init_opts = init.add_mutually_exclusive_group()
    init_opts.add_argument('--config', action='store_true',
                           help='only create a new config string and print it out')
    init_opts.add_argument('--force', action='store_true',
                           help='remove an existing rc-file and init pynote')

    # note revisions
    revisions = subparsers.add_parser('revisions')
    revisions.add_argument('key', type=int)

    # note tags
    tags = subparsers.add_parser('tags')
    tags.add_argument('key', type=int, nargs='?')
    tags_opts = tags.add_mutually_exclusive_group()
    tags_opts.add_argument('-a', '--add', nargs='+')
    tags_opts.add_argument('-d', '--delete', nargs='+')

    # note export
    export = subparsers.add_parser('export', help='export notes')
    export.add_argument('key', type=int, nargs='?')
    export.add_argument('-n', '--no-header', action='store_true',
                        help='do not show header data')
    export.add_argument('--force', action='store_true',
                        help='overwrite existing export directory')

    # note --version
    parser.add_argument('--version', help='show version', action='version',
                        version='pynote {}'.format(pynote.__version__))

    args = parser.parse_args()

    # Choose the correct function from pynote.command
    # depending on args.cmd.  Choose note list if no
    # command is entered.
    if args.cmd is None:
        note.list_()

    elif args.cmd == 'list':
        note.list_(args.tags)

    elif args.cmd == 'show':
        if args.all:
            note.show_all(args.no_header)
        else:
            note.show(args.key, args.no_header, args.lang)

    elif args.cmd == 'new':
        note.new(args.title)

    elif args.cmd == 'edit':
        note.edit(args.key, args.title)

    elif args.cmd == 'delete':
        note.delete(args.key)

    elif args.cmd == 'trash':
        note.trash()

    elif args.cmd == 'restore':
        note.restore(args.key)

    elif args.cmd == 'compare':
        if args.new_rev > args.old_rev:
            note.compare(args.key, args.new_rev, args.old_rev, args.color)
        else:
            print('Error: old_rev must not be smaller than new_rev!')
            exit(1)

    elif args.cmd == 'revisions':
        note.revisions(args.key)

    elif args.cmd == 'tags':
        if args.add and args.key:
            note.add_tags(args.key, args.add)
        elif args.delete and args.key:
            note.del_tags(args.key, args.delete)
        elif args.add and not args.key:
            print('Error: missing key!')
            exit(1)
        elif args.delete and not args.key:
            print('Error: missing key!')
            exit(1)
        elif args.key:
            note.note_tags(args.key)
        else:
            note.tags()

    elif args.cmd == 'export':
        if args.key:
            note.export(args.key, args.no_header, args.force)
        else:
            note.export_all(args.no_header, args.force)

    elif args.cmd == 'init':
        if args.config:
            pynote.init.create_config_string()
        else:
            pynote.init.create_noterc(args.force)


if __name__ == '__main__':
    run()
