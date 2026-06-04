"""Unit tests for download.py — verify URL and filename constants."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDownloadConstants:
    def test_url_is_valid_http(self):
        """Verify the download URL is a valid HTTPS/HTTP URL."""
        # Import the module-level variables without executing the download
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "download",
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "download.py",
            ),
        )
        # We can't actually import download.py because it runs urllib.request.urlretrieve
        # on import. Instead we just verify the URL string is well-formed by reading the file.
        download_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "download.py",
        )
        with open(download_path) as f:
            source = f.read()

        assert "https://" in source or "http://" in source
        assert "notMNIST" in source
        assert ".tar.gz" in source

    def test_filename_has_correct_extension(self):
        download_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "download.py",
        )
        with open(download_path) as f:
            source = f.read()

        assert "notMNIST_small.tar.gz" in source
