#!/usr/bin/env python3
'''
Parameterize a unit test
'''
from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock, MagicMock
from utils import access_nested_map, get_json, memoize
from typing import (
    Mapping,
    Sequence,
    Any,
)


class TestAccessNestedMap(unittest.TestCase):
    '''Tests utils.access_nested_map'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        '''test that the method returns what it is supposed to'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, err):
        '''test that a KeyError is raised for the following inputs'''
        self.assertRaises(err)


class TestGetJson(unittest.TestCase):
    '''Tests utils.get_json method'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_json):
        '''test that utils.get_json returns the expected result'''
        mock_res = Mock()
        mock_res.json.return_value = test_payload
        mock_json.return_value = mock_res

        self.assertEqual(get_json(test_url), test_payload)
        mock_json.assert_called_once_with(test_url)
