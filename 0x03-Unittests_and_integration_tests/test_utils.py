#!/usr/bin/env python3
""" doc doc doc """
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Tuple, Dict
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map utility function from utils module.

    access_nested_map takes a dictionary and a path as input and returns
    the value associated with that path in the dictionary. The path is a
    tuple of keys.

    If the path does not exist in the dictionary, a KeyError is raised.

    Parameters
    ----------
    nested_map : Dict[str, Any]
        a nested map
    path : Tuple[str]
        a sequence of key representing a path to the value
    expected : Any
        the expected value

    Examples
    -------
    >>> nested_map = {"a": 1}
    >>> access_nested_map(nested_map, ("a",))
    1
    >>> nested_map = {"a": {"b": 2}}
    >>> access_nested_map(nested_map, ("a",))
    {'b': 2}
    >>> access_nested_map(nested_map, ("a", "b"))
    2

    Tests
    ------
    >>> nested_map = {}
    >>> with self.assertRaises(KeyError):
    ...     access_nested_map(nested_map, ("a",))
    >>> nested_map = {"a": 1}
    >>> with self.assertRaises(KeyError):
    ...     access_nested_map(nested_map, ("a", "b"))
    """


    @parameterized.expand(
        [
            (
                {"a": 1},
                ("a",),
                1,
                # Test a simple value
            ),
            (
                {"a": {"b": 2}},
                ("a",),
                {"b": 2},
                # Test a nested value
            ),
            (
                {"a": {"b": 2}},
                ("a", "b"),
                2,
                # Test a nested value with multiple steps
            ),
        ]
    )
    def test_access_nested_map(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str],
        expected: Any,
        # test data for access_nested_map
    ) -> None:
        """Test access_nested_map utility function.

        Verify that access_nested_map returns the expected value when given
        a nested dictionary and a path to the value.

        Parameters
        ----------
        nested_map : Dict[str, Any]
            a nested map
        path : Tuple[str]
            a sequence of key representing a path to the value
        expected : Any
            the expected value
        """
        self.assertEqual(
            access_nested_map(nested_map, path), expected
        )  # verify the expected value is returned

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str]
    ) -> None:
        """doc doc doc"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json utility function from utils module.

    get_json takes a URL as input and returns the JSON payload from the
    request to the URL. It uses the requests library to make the GET
    request.

    If the request is successful, the JSON payload is returned. If the
    request is not successful, a RuntimeError is raised.

    Parameters
    ----------
    test_url : str
        the URL to get the JSON payload from
    test_payload : Dict[str, Any]
        the expected JSON payload
    mock_get : Mock
        a mock object for the requests.get function
    """

    @parameterized.expand(
        [
            # test case 1: successful get request
            ("http://example.com", {"payload": True}),
            # test case 2: failed get request
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        """Test get_json utility function from utils module.

        Tests that get_json returns the expected JSON payload from a
        successful GET request, and raises a RuntimeError if the request
        is not successful.

        Parameters
        ----------
        test_url : str
            the URL to get the JSON payload from
        test_payload : Dict[str, Any]
            the expected JSON payload
        mock_get : Mock
            a mock object for the requests.get function
        """
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """doc doc doc"""

    def test_memoize(self) -> None:
        """Tests that the @memoize decorator works correctly.

        The test case demonstrates that the decorated method is only
        called once, even if the property is accessed multiple times.
        """

        class TestClass:
            """doc doc doc"""

            def a_method(self) -> int:
                """doc doc doc"""
                return 42

            @memoize
            def a_property(self) -> int:
                """doc doc doc"""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mocked.assert_called_once()
