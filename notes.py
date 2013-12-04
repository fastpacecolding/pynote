import argparse

from note import Note
from note import TableReport


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='subparser',
                                      help='sub-command help')

    parser_add = subparser.add_parser('list')
    # parser_add.add_argument('note', type=str, help='bar help')

    parser_add = subparser.add_parser('new')
    parser_add.add_argument('title', type=str)

    parser_add = subparser.add_parser('show')
    parser_add.add_argument('uuid', type=str)

    parser_delete = subparser.add_parser('delete')
    parser_delete.add_argument('note', type=str, help='bar help')
    args = parser.parse_args()

    return(args)


def main():
    args = parse_args()

    if args.subparser == 'list':
        TableReport()
    elif args.subparser == 'new':
        Note.create(args.title)
    elif args.subparser == 'show':
        Note.show(args.uuid)


if __name__ == '__main__':
    main()
