
import hashlib

class UrlHash:
    @staticmethod
    def encode_url(url):
        """
        Encodes a URL into a unique hash string using SHA-256.

        Parameters:
        - url (str): The URL to be encoded.

        Returns:
        - str: A SHA-256 hash of the URL.
        """
        # Encode the URL to a bytes object required by hashlib
        url_bytes = url.encode( 'utf-8' )

        # Create a sha256 hash object
        hasher = hashlib.sha256()

        # Update the hash object with the bytes of the URL
        hasher.update( url_bytes )

        # Return the hexadecimal digest of the URL
        return hasher.hexdigest()