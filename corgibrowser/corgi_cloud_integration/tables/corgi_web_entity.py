import re
import urllib
from urllib.parse import urlparse

from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator


class CorgiWebEntity:
    def __init__(self, partition_key, row_key, full_url, status, father_url = ""):

        self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(full_url)
        self.RowKey = CorgiNameGenerator.generate_blob_name(row_key)

        # Blob Storage
        self.ContainerName = self.PartitionKey
        self.BlobName = self.RowKey

        #Table Storage
        self.TableName = self.PartitionKey

        # URL Original Data
        self.OriginalDomain = partition_key  # Domain
        self.OriginalUrl = row_key  # Url
        self.FullUrl = full_url
        self.FatherUrl = father_url

        self.Status = status

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,

            "TableName": self.TableName,

            # Blob Storage
            "ContainerName": self.ContainerName,
            "BlobName": self.BlobName,

            # URL Original Data
            "OriginalDomain": self.OriginalDomain,
            "OriginalUrl": self.OriginalUrl,
            "FullUrl": self.FullUrl,
            "FatherUrl": self.FatherUrl,

            # Others
            "Status": self.Status,
            # Add other properties here
        }
