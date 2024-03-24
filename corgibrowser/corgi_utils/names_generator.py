# utils.py

import re
import urllib
from urllib.parse import urlparse

class CorgiNameGenerator:
    @staticmethod
    def get_storage_compatible_name(url):
        """
        Generate a storage-compatible name based on the domain of the given URL,
        ensuring it contains only letters and digits (no dashes), and adheres to Azure Storage naming rules.

        Parameters:
        - url (str): The input URL from which to extract the domain for name generation.

        Returns:
        - str: A name derived from the domain, compatible with Azure Storage naming rules, containing only letters and digits.
        """
        def format_name(domain):
            # Convert to lowercase as container names must be lowercase
            domain = domain.lower()
            # Remove all characters except letters and digits
            domain = re.sub(r'[^a-z0-9]', '', domain)
            # Ensure the name starts with a letter or digit
            if not domain[0].isalpha() and not domain[0].isdigit():
                domain = 'a' + domain
            # Ensure name length is within Azure's constraints
            domain_length = len(domain)
            if domain_length < 3:
                domain += 'a' * (3 - domain_length)  # Pad if less than 3 characters
            elif domain_length > 63:
                domain = domain[:63]  # Truncate if more than 63 characters
            return domain

        parsed_url = urlparse( url )
        domain = parsed_url.netloc or parsed_url.path  # Use path if netloc is empty
        domain = domain.split( ':' )[ 0 ]  # Remove port number if present
        return format_name( domain )

    @staticmethod
    def get_container_compatible_name(container_name):
        def format_name(name):
            # Convert to lowercase as container names must be lowercase
            name = name.lower()
            # Remove all characters except letters, digits, and single dashes
            name = re.sub(r'[^a-z0-9-]', '', name)
            # Replace multiple consecutive dashes with a single dash
            name = re.sub(r'-{2,}', '-', name)
            # Ensure the name starts and ends with a letter or digit
            name = re.sub(r'^-+|-+$', '', name)
            if len(name) == 0:
                name = "default"
            if not name[0].isalpha() and not name[0].isdigit():
                name = 'a' + name
            # Ensure name length is within Azure's constraints
            if len(name) < 3:
                name = name.ljust(3, 'a')  # Pad if less than 3 characters
            elif len(name) > 63:
                name = name[:63]  # Truncate if more than 63 characters
            return name

        return format_name(container_name)

    @staticmethod
    def generate_blob_name(url):
        """
        Generate a unique blob name based on the URL.
        """
        # Simplified example, consider a more robust approach for real applications
        return urllib.parse.quote_plus(url)

    @staticmethod
    def extract_domain(url):
        """Extract the domain from a URL.
            a) Domain Extraction: Extracting the domain from each URL is crucial for steps
            like fetching robots.txt. It helps in categorizing URLs and applying domain-specific
            crawling rules.
        """
        parsed_url = urlparse(url)
        print( f"     CrawlerProcessor: Domain for Url {parsed_url.netloc}" )
        return parsed_url.netloc



