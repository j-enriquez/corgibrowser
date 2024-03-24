import unittest

from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator

class TestCorgiNameGenerator(unittest.TestCase):
    def test_simple_domain(self):
        url = "http://example.com"
        expected_name = "examplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_with_subdomain(self):
        url = "http://blog.example.com"
        expected_name = "blogexamplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_with_port(self):
        url = "http://example.com:8080"
        expected_name = "examplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_with_dash(self):
        url = "http://example-site.com"
        expected_name = "examplesitecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_with_special_chars(self):
        url = "http://example_site.com"
        expected_name = "examplesitecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_long_domain(self):
        url = "http://a-very-long-domain-name-that-exceeds-the-maximum-length-allowed-by-azure-storage.com"
        expected_name = "averylongdomainnamethatexceedsthemaximumlengthallowedbyazuresto"  # truncated to 63 chars
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_short_domain(self):
        url = "http://ex.com"
        expected_name = "excom"  # padded to meet the minimum length requirement
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_with_query(self):
        url = "http://example.com?query=123"
        expected_name = "examplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_https_domain(self):
        url = "https://example.com"
        expected_name = "examplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_ftp_domain(self):
        url = "ftp://example.com"
        expected_name = "examplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_domain_prefix(self):
        url = "ftp://www.example.com"
        expected_name = "wwwexamplecom"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)

    def test_ftp_domain_co(self):
        url = "ftp://www.example.com.co"
        expected_name = "wwwexamplecomco"
        self.assertEqual(CorgiNameGenerator.get_storage_compatible_name(url), expected_name)