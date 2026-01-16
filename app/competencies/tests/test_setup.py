from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    """Class with setup and teardown for tests in CIS Competencies"""

    def setUp(self):
        """Function to set up necessary data for testing"""

        self.patcher = patch('competencies.signals.create_neo_domain')
        self.block_create_neo_domain = self.patcher.start()

        self.profile = {
            'name': {
                'data_type': 'str'
            },
            'uuid': {
                'data_type': 'str'
            },
            'profile': {
                'data_type': 'str',
                'use': 'required'
            },
            'WITHIN': {
                'data_type': 'str',
                'use': 'Optional',
                'relationship': True
            }
        }
        self.restricted_profile = {
            'name': {
                'data_type': 'str',
                'use': 'required'
            },
            'uuid': {
                'data_type': 'str'
            },
            'profile': {
                'data_type': 'str',
                'use': 'required'
            },
            'WITHIN': {
                'data_type': 'str',
                'use': 'Optional',
                'relationship': True
            }
        }

        # create user, save user, login using client
        self.auth_email = "test_auth@test.com"
        self.auth_password = "test_auth1234"
        self.auth_first_name = "first_name_auth"
        self.auth_last_name = "last_name_auth"

        self.auth_user = User.objects.create_user(self.auth_email,
                                                  self.auth_password,
                                                  first_name=self.auth_first_name,
                                                  last_name=self.auth_last_name,
                                                  is_superuser=True)

        return super().setUp()

    def tearDown(self):
        self.patcher.stop()
        return super().tearDown()
