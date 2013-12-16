def expand_dateformat(dateformat):
    tmp = ''

    for s in dateformat:
        if s.isalpha():
            tmp += '%' + s
        else:
            tmp += s
    return tmp
