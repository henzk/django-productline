from django.test import TestCase
import ape
from django.conf import settings

class SyncPermissionTestCase(TestCase):

    def test_auth_groups(self):
        """
        Tests the synchronizations of auth groups.
        :return:
        """
        settings.AUTH_GROUPS = [
            {
                'name': 'Operator',
                'permissions': [
                    ('add_user', 'auth'),
                    ('change_user', 'auth')
                ]
            }    
        ]
        
        ape.tasks.sync_auth_groups()
