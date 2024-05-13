#!/usr/bin/env python3
""" doc doc doc """
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import unittest
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """doc doc doc"""

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        """doc doc doc"""
        # Verify GithubOrgClient.org returns the payload and
        # verify get_json was called with the correct url
        github_org_client = GithubOrgClient(org_name)
        self.assertEqual(github_org_client.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        """doc doc doc"""
        # Verify GithubOrgClient._public_repos_url returns the
        # correct value when org is patched
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = payload
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client._public_repos_url,
                         payload["repos_url"])

    @patch("client.get_json",
           return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:
        """doc doc doc"""
        # Verify GithubOrgClient.public_repos returns the correct
        # value and verify get_json was called with the correct url
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            github_org_client = GithubOrgClient("google")
            self.assertEqual(github_org_client.public_repos(),
                             ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected_result) -> None:
        """doc doc doc"""
        # Verify GithubOrgClient.has_license returns the correct value
        github_org_client = GithubOrgClient("google")
        self.assertEqual(
            github_org_client.has_license(repo, license_key), expected_result
        )


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Tests of the GithubOrgClient class using the MockResponse and side_effect
    fixture."""

    @classmethod
    def setUpClass(cls):
        """Set up the mock for the requests.get call.

        This is done in setUpClass so that all the tests use the same mock.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Return a MockResponse based on the url.

            If the url ends with "/orgs/google", return the org_payload.
            If the url ends with "/orgs/google/repos", return the repos_payload.
            Otherwise, return None.
            """
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the mock.

        This is done in tearDownClass so that all tests finish using the same mock.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos returns the correct value."""
        github_org_client = GithubOrgClient("google")
        self.assertEqual(github_org_client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test GithubOrgClient.public_repos returns the correct value with a license."""
        github_org_client = GithubOrgClient("google")
        self.assertEqual(
            github_org_client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
