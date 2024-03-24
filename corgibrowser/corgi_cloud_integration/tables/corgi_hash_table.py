import re
import urllib
from urllib.parse import urlparse

from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator
from corgibrowser.corgi_utils.url_hash import UrlHash

class CorgiHashTable:
    def __init__(self, full_url):
        self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(full_url)
        self.RowKey = UrlHash.encode_url(full_url)
        self.FullUrl = full_url

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,
            "FullUrl": self.FullUrl
        }
