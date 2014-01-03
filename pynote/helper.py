from tempfile import NamedTemporaryFile


def expand_dateformat(dateformat):
    """
    Takes the dateformat string from ~/.noterc
    and adds the '%'-signs.

    Y.m.d. => %Y.%m.%d.

    """
    format_str = ''

    for v in dateformat:
        if v.isalpha():
            format_str += '%' + v
        else:
            format_str += v
    return format_str


def create_tempfile():
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()
    return tmp_file.name


def exit_not_exists():
    print(_('Error: This note does not exist!'))
    exit(1)
