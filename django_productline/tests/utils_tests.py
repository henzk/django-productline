from __future__ import unicode_literals, print_function

import os
import os.path
import shutil

from django_productline import utils
from django_productline.testingutils import NoMigrationsTestCase

__all__ = ['UtilsTestCase']


class UtilsTestCase(NoMigrationsTestCase):
    def test_zipdir(self):
        """
        Tests the zipdir function
        :return:
        """
        testdatadir = os.path.join(os.path.dirname(__file__), '__testdata__')
        zipthisfolder = os.path.join(testdatadir, 'zipthisfolder')
        os.makedirs(zipthisfolder)
        os.mknod(os.path.join(zipthisfolder, 'file'))
        src_path = os.path.join(testdatadir, 'zipthisfolder')
        target_path = os.path.join(testdatadir, 'result.zip')
        utils.zipdir(src_path, target_path)
        self.assertTrue(os.path.exists(target_path))
        shutil.rmtree(zipthisfolder)
        os.remove(target_path)
