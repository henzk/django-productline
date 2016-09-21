from django_productline.testingutils import NoMigrationsTestCase
from django_productline import utils
import os.path


__all__ = ['UtilsTestCase']

class UtilsTestCase(NoMigrationsTestCase):


    def test_zipdir(self):
        """
        Tests the zipdir function
        :return:
        """
        testdatadir = os.path.join(os.path.dirname(__file__), '__testdata__')
        src_path = os.path.join(testdatadir, 'zipthisfolder')
        target_path = os.path.join(testdatadir, 'result.zip')
        utils.zipdir(src_path, target_path)
        self.assertTrue(os.path.exists(target_path))
        






