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

    @patch('client.get_json')
    def test_public_repos(self, mocked_json):
        '''self descriptive'''
        payload = [{"name": "Google"}, {"name": "abc"}]
        mocked_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mocked_url:

            mocked_url.return_value = 'url'
            response = GithubOrgClient('test').public_repos()

            self.assertEqual(response, ["Google", "abc"])

            mocked_url.assert_called_once()
            mocked_json.assert_called_once()

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
        def side_effect(*args):
            '''returns the correct fixtures for the various values of url'''
            if args[0] == 'https://api.github.com/orgs/google/repos':
                return self.repos_payload
            elif args[0] == 'https://api.github.com/orgs/google':
                return self.org_payload
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)]

    @classmethod
    def tearDownClass(cls):
        '''tear down class'''
        cls.get_patcher.stop()

    def test_public_repos(self):
        '''Test GithubOrgClient.public_repos'''
        self.assertEqual(GithubOrgClient('google').public_repos(),
                         self.expected_repos)

    def test_public_repos_with_license(self):
        '''test the public_repos with the argument license="apache-2.0"'''
        repo = GithubOrgClient('google').public_repos(license="apache-2.0")
        self.assertEqual(repo, self.apache2_repos)
