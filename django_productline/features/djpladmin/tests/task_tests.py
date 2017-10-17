from __future__ import unicode_literals

import ape

from django.test import TestCase
from django.conf import settings


class SyncPermissionTestCase(TestCase):

    def test(self):
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
