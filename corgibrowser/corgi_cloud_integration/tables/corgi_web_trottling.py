import datetime
from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator

class CorgiWebThrottling:
    def __init__(self, domain, rate=None, last_access_time=None):
        self.PartitionKey = "RateLimit"
        self.RowKey = domain
        self.ThrottlingLimitSeconds = rate
        self.LastAccessTime = last_access_time

    @classmethod
    def from_entity(cls, entity):
        domain = entity['RowKey']
        rate = entity['ThrottlingLimitSeconds']
        last_access_time = entity._metadata['timestamp'].replace(tzinfo=None)
        return cls(domain, rate, last_access_time)

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,
            "ThrottlingLimitSeconds": self.ThrottlingLimitSeconds
        }