__version__ = '0.3'
__author__ = 'Hendrik Speidel <hendrik@schnapptack.de>'

import re

def compare_version(version1, version2):
    """
    Compares two versions.
    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))
