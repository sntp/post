import re


def check_if_number(string):
    pattern = re.compile('^\d*$')
    return True if pattern.match(string or '') else False
