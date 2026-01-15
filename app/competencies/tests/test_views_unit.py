import json
from unittest.mock import Mock, patch

from django.test import tag
from django.urls import reverse
from rest_framework import status

from ..models import GenericNode
from .test_setup import TestSetUp


@tag('unit')
class ViewTests(TestSetUp):

    # managed-data fail and success

    def test_get_metadata_domain_list(self):
        """
        Test that the /api/managed-data/ endpoint returns a list of domains
        """

        url = reverse('competencies:managed-catalog')
        with patch('competencies.views.NeoDomain') as nd:
            domain_0 = 'test'
            domain_1 = 'another'
            nd.nodes.all.return_value = [
                GenericNode({'name': domain_0}.items()),
                GenericNode({'name': domain_1}.items()),
            ]

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK)
            self.assertTrue(domain_0 in responseDict)
            self.assertTrue(domain_1 in responseDict)

    def test_get_metadata_domain_list_no_domains(self):
        """
        Test that the /api/managed-data/ endpoint fails correctly when no domains
        """

        url = reverse('competencies:managed-catalog')
        with patch('competencies.views.NeoDomain') as nd:
            nd.nodes.all.return_value = []
            response = self.client.get(url)
            responseDict = json.loads(json.loads(response.content))

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK)
            self.assertTrue(len(responseDict) == 0)

    # api/managed-metadata
    def test_get_managed_metadata(self):
        """
        Test that the /api/managed-data/ returns a
        list of records under the domain
        """
        domain = 'test'
        expected = [{'name': 'test obj', 'uuid': 'abc123'},
                    {'name': 'second test obj', 'uuid': '987zyx'}]
        url = reverse('competencies:managed-catalog-data', args=(domain,))

        with patch('competencies.views.LazyNeoQuery') as lnq, \
                patch('competencies.views.NeoDomain') as nd:
            lnq.return_value = lnq
            lnq.count = len(expected)
            lnq.__len__.return_value = len(expected)
            lnq.__getitem__ = Mock()
            lnq.__getitem__.side_effect = [expected,]

            nd.uuid = domain

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK)
            self.assertEqual(responseDict['count'], len(expected))
            for got, exp in zip(responseDict['results'], expected):
                self.assertDictEqual(got, exp)

    def test_get_managed_metadata_key_hashes_not_found(self):
        """
        Test that the /api/managed-data/ returns an
        error if no record is found
        """
        domain = 'test'
        expected = []
        url = reverse('competencies:managed-catalog-data', args=(domain,))

        with patch('competencies.views.LazyNeoQuery') as lnq, \
                patch('competencies.views.NeoDomain') as nd:
            lnq.return_value = lnq
            lnq.count = len(expected)
            lnq.__len__.return_value = len(expected)
            lnq.__getitem__ = Mock()
            lnq.__getitem__.side_effect = [expected,]

            nd.uuid = domain

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK)
            self.assertEqual(responseDict['count'], len(expected))
            self.assertEqual(responseDict['results'], expected)

    # post /api/metadata/
    def test_post_record_valid(self):
        """
        Test that sending a POST request to the /api/metadata endpoint
        succeeds and returns unique record identifier for the new record
        """
        url = reverse('competencies:metadata')

        obj = {'name': 'test obj', 'uuid': 'abc123', 'profile': 'made up'}

        with patch('competencies.serializers.read_json_data') as get_profile, \
                patch('competencies.serializers.db') as gdb:
            get_profile.return_value = self.profile
            gdb.cypher_query.return_value = [[[obj]]]

            dataSTR = json.dumps(obj)
            dataJSON = json.loads(dataSTR)

            self.client.force_login(self.auth_user)
            response = self.client.post(
                url, dataJSON, format="json")
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED)
            self.assertEqual(responseDict, obj)

    def test_post_record_invalid(self):
        """
        Test that sending a POST request to the /api/metadata endpoint
        fails correctly
        """
        url = reverse('competencies:metadata')

        obj = {'uuid': 'abc123', 'profile': 'made up'}

        with patch('competencies.serializers.read_json_data') as get_profile:
            get_profile.return_value = self.restricted_profile

            dataSTR = json.dumps(obj)
            dataJSON = json.loads(dataSTR)

            self.client.force_login(self.auth_user)
            response = self.client.post(
                url, dataJSON, format="json")
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)
            self.assertTrue(responseDict)

    # api/managed-metadata

    def test_post_managed_metadata(self):
        """
        Test that sending a POST request to the /api/managed-data endpoint
        succeeds and updates the record
        """
        domain = 'test'
        uuid = 'abc123'
        obj = {'name': 'test obj', 'uuid': uuid, 'profile': 'made up'}

        url = reverse('competencies:managed-data', args=(domain, uuid,))

        with patch('competencies.serializers.read_json_data') as get_profile, \
                patch('competencies.views.db') as gdb, \
                patch('competencies.serializers.db') as sdb:

            get_profile.return_value = self.profile
            gdb.cypher_query.side_effect = [[[[obj]]], [[]]]
            sdb.cypher_query.return_value = [[[obj]]]

            dataSTR = json.dumps(obj)
            dataJSON = json.loads(dataSTR)

            self.client.force_login(self.auth_user)
            response = self.client.put(
                url, dataJSON, format="json")
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code,
                             status.HTTP_200_OK)
            self.assertEqual(responseDict, obj)

    def test_post_managed_metadata_invalid(self):
        """
        Test that sending a POST request to the /api/metadata endpoint
        fails and returns a 400
        """
        domain = 'test'
        uuid = 'abc123'
        obj = {'uuid': uuid, 'profile': 'made up'}

        url = reverse('competencies:managed-data', args=(domain, uuid,))

        with patch('competencies.serializers.read_json_data') as get_profile, \
                patch('competencies.views.db') as gdb:

            get_profile.return_value = self.restricted_profile
            gdb.cypher_query.side_effect = [[[[obj]]], [[]]]

            dataSTR = json.dumps(obj)
            dataJSON = json.loads(dataSTR)

            self.client.force_login(self.auth_user)
            response = self.client.put(
                url, dataJSON, format="json")

            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)
