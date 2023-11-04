#!/usr/bin/env python3
'''
Parameterize a unit test
'''
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, Mock, PropertyMock
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''Tests utils.access_nested_map'''
    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, name, mock):
        '''test that GithubOrgClient.org returns the correct value'''
        obj = GithubOrgClient(name)
        obj.org()
        mock.assert_called_once_with(obj.ORG_URL.format(org=name))

    @parameterized.expand([
        ('google', {'repos_url': 'https://github.com/name/repo'})
    ])
    def test_public_repos_url(self, name, result):
        '''method to unit-test GithubOrgClient._public_repos_url'''
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mocke:
            mocke.return_value = result
            self.assertEqual(GithubOrgClient(name)._public_repos_url,
                             result.get('repos_url'))

    @parameterized.expand([
        ('google')
    ])
    @patch('client.get_json')
    def test_public_repos(self, name, mock_json):
        '''Tests GithubOrgClient.public_repos'''
        mock_json.return_value = [{'name': 'Chrome', 'date': '23-02-23'},
                                  {'name': 'Cloud', 'date': '23-03-22'}]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repo:
            mock_repo.return_value = 'url'
            res = GithubOrgClient(name).public_repos()
            self.assertEqual(res, ['Chrome', 'Cloud'])
            mock_repo.assert_called_once()
        mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, val):
        '''unit-test GithubOrgClient.has_license'''
        self.assertEqual(GithubOrgClient('tst').has_license(repo, license_key),
                         val)


@parameterized_class([
    {'org_payload': TEST_PAYLOAD[0][0], 'repos_payload': TEST_PAYLOAD[0][1],
     'expected_repos': TEST_PAYLOAD[0][2], 'apache2_repos': TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Integration test for GithubOrgClient class'''
    @classmethod
    def setUpClass(cls):
        '''set up class'''
        def side_effect(url):
            '''returns the correct fixtures for the various values of url'''
            if url == 'https://api.github.com/orgs/google/repos':
                return self.repos_payload
            elif url == 'https://api.github.com/orgs/google':
                return self.org_payload
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_res = Mock()
        mock_res.json.side_effect = side_effect
        mock_get.return_value = mock_res

    @classmethod
    def tearDownClass(cls):
        '''tear down class'''
        cls.get_patcher.stop()
