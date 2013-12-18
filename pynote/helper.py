from tempfile import NamedTemporaryFile


def expand_dateformat(dateformat):
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
