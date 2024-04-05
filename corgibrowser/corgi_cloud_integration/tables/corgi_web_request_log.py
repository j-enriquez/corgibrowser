import datetime
from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator

class CorgiWebRequestLog:
    def __init__(self, domain, url, status_code, instance_id):
        utc_now = datetime.datetime.utcnow()
        row_key = utc_now.strftime( '%Y%m%dT%H%M%SZ' )

        self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name( domain )
        self.RowKey = row_key
        self.Url = url
        self.StatusCode = status_code
        self.InstanceId = instance_id

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,
            "Url": self.Url,
            "StatusCode": self.StatusCode,
            "InstanceId": self.InstanceId
        }