#!/usr/bin/env python3
'''
Parameterize a unit test
'''
from parameterized import parameterized
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


    @patch('GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        '''method to unit-test GithubOrgClient._public_repos_url'''
        mock_org.return_value = 
        self.assertEqual(_public_repos_url(),
