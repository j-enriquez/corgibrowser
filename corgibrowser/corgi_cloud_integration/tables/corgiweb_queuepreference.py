from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator


class CorgiWebQueuePreference:
    def __init__(self, partition_key,row_key, items_to_pop_from_queue, visibility_timeout):

        self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(partition_key)
        self.RowKey = CorgiNameGenerator.get_storage_compatible_name(row_key)
        self.ItemsToPopFromQueue = items_to_pop_from_queue
        self.VisibilityTimeout = visibility_timeout

    def to_dict(self):
        return {
            "PartitionKey": self.PartitionKey,
            "RowKey": self.RowKey,
            "ItemsToPopFromQueue": self.ItemsToPopFromQueue,
            "VisibilityTimeout": self.VisibilityTimeout
        }
