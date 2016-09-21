from __future__ import unicode_literals, print_function, division
import os
import zipfile
import re


def zipdir(src_path, target_path):
    """
    Zips the pat
    :param path: the path to the directory
    :param ziph: zthe zipfile handle
    :return:
    """

    zipf = zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(src_path):
        for file in files:
            path = os.path.join(root, file)
            # get the relative path from the src_path in order to avoid an archive
            # of absolute paths including your home directory.
            rel_path = os.path.relpath(path, src_path)
            zipf.write(path, rel_path)

    zipf.close()


def compare_version(version1, version2):
    """
    Compares two versions.
    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))
