from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator


class CorgiWebStorageAnalytics:
    def __init__(self, partition_key, object_type, object_name, status, count):

        self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(partition_key)
        # object_type Accepted Values: Table,Queue,Container
        self.RowKey = object_type + "_" + object_name

        self.ObjectType = object_type
        self.ObjectName = object_name

        self.Status = status
        self.Count = count

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,

            "ObjectType": self.ObjectType,
            "ObjectName": self.ObjectName,

            # Blob Storage
            "Status": self.Status,
            "Count": self.Count
        }