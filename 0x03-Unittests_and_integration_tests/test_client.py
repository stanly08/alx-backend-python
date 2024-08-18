#!/usr/bin/env python3
"""TestGithubOrgClient module
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient class
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org, get):
        """
        test_org - verifies that GithubOrgClient.org returns the expected value
        """
        client = GithubOrgClient(org)
        test_return = client.org
        self.assertEqual(test_return, get.return_value)
        get.assert_called_once

    def test_public_repos_url(self):
        """
        test_public_repos_url - unit-test GithubOrgClient._public_repos_url
        """
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value={"repos_url": "holberton"}) as mock_get:
            test_json = {"repos_url": "holberton"}
            test_client = GithubOrgClient(test_json.get("repos_url"))
            test_return = test_client._public_repos_url
            mock_get.assert_called_once
            self.assertEqual(test_return,
                             mock_get.return_value.get("repos_url"))

    @patch("client.get_json", return_value=[{"name": "holberton"}])
    def test_public_repos(self, mock_get):
        """
        test_public_repos - list of repos is as expect from the chosen payload
        """
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/") as mock_buc:
            test_client = GithubOrgClient("holberton")
            test_return = test_client.public_repos()
            self.assertEqual(test_return, ["holberton"])
            mock_get.assert_called_once
            mock_buc.assert_called_once

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        test_has_license - to unit-test GithubOrgClient.has_license
        """
        test_client = GithubOrgClient("holberton")
        test_return = test_client.has_license(repo, license_key)
        self.assertEqual(test_return, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    test the GithubOrgClient.public_repos method in an integration test
    """

    @classmethod
    def setUpClass(cls):
        """
        setUpClass - set up
        """
        conf = {"return_value.json.side_effect":
                [
                    cls.org_payload, cls.repos_payload,
                    cls.org_payload, cls.repos_payload
                ]}
        cls.get_patcher = patch("requests.get", **conf)

        cls.mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        tearDownClass - tear Down
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        test_public_repos - method to test GithubOrgClient.public_repos
        """
        test_class = GithubOrgClient("holberton")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """
        test_public_repos_with_license -  with the argument license="apache-2.0
        """
        test_class = GithubOrgClient("holberton")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos("apache-2.0"),
                         self.apache2_repos)
        self.mock.assert_called()
