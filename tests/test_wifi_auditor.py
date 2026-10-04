import unittest
from unittest.mock import patch

from wifi_auditor import get_profiles


class TestWiFiAuditor(unittest.TestCase):

    @patch("wifi_auditor.run_netsh")
    def test_profile_parsing(self, mock_run_netsh):
        mock_run_netsh.return_value = """
        All User Profile : HomeWiFi
        All User Profile : Office WiFi
        All User Profile : Test_5G
        """

        profiles = get_profiles()

        self.assertEqual(
            profiles,
            ["HomeWiFi", "Office WiFi", "Test_5G"],
        )

    @patch("wifi_auditor.run_netsh")
    def test_unicode_profile(self, mock_run_netsh):
        mock_run_netsh.return_value = (
            "All User Profile : €¥~shishir ~$¢™©®§"
        )

        profiles = get_profiles()

        self.assertEqual(
            profiles,
            ["€¥~shishir ~$¢™©®§"],
        )

    @patch("wifi_auditor.run_netsh")
    def test_empty_profile_output(self, mock_run_netsh):
        mock_run_netsh.return_value = ""

        profiles = get_profiles()

        self.assertEqual(profiles, [])

    @patch("wifi_auditor.run_netsh")
    def test_profile_count(self, mock_run_netsh):
        mock_run_netsh.return_value = """
        All User Profile : WiFi_1
        All User Profile : WiFi_2
        All User Profile : WiFi_3
        All User Profile : WiFi_4
        """

        profiles = get_profiles()

        self.assertEqual(len(profiles), 4)


if __name__ == "__main__":
    unittest.main()