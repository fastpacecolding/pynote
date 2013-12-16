from tempfile import NamedTemporaryFile


def expand_dateformat(dateformat):
    tmp = ''

    for s in dateformat:
        if s.isalpha():
            tmp += '%' + s
        else:
            tmp += s
    return tmp


def create_tempfile():
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.close()
    return tmp_file.name
