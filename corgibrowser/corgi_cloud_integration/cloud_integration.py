from azure.identity import DefaultAzureCredential
from corgibrowser.corgi_cloud_integration.azure_direct_operations import AzureDirectOperations
from corgibrowser.corgi_cloud_integration.queues_schemas.corgi_web_queue_version_1 import CorgiWebMessageSchemaVersion1
from corgibrowser.corgi_cloud_integration.tables.corgi_hash_table import CorgiHashTable
from corgibrowser.corgi_cloud_integration.tables.corgiweb_queuepreference import CorgiWebQueuePreference
import urllib.parse
import datetime
from datetime import timedelta
from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator


class CloudIntegration:
    """
    Class for comprehensive integration with Azure services.
    Handles operations like blob storage management, authentication, and more.
    """

    def __init__(self, settings_manager):
        self.credential = DefaultAzureCredential()
        self.cloud_direct_operations = AzureDirectOperations( settings_manager.CLOUD )
        self.config = settings_manager.CLOUD
        self.initialized = False

    def initialize(self):

        # 1. Initialize System tables
        for table_name in [ "corgiwebthrottling", "corgiwebsitemaps", "corgiwebrequestslog",
                            "corgiwebqueuepreference", "corgiwebhashtable" ]:
            self.cloud_direct_operations.create_and_get_table( table_name )

        # 2.- Initialize System queues
        for queue_name in [ "corgiweb" ]:
            self.cloud_direct_operations.create_and_get_queue( queue_name )

        # 3.- Initialize System containers
        for container_name in [ "corgirobotscache" ]:
            self.cloud_direct_operations.create_and_get_container( container_name )

        self.initialized = False

    def add_domain_to_queue_preference_table(self,container_table_queue_name,items_to_pop_from_queue,visibility_timeout):
        # 3. Add message to Queue Preference Table
        row = CorgiWebQueuePreference( partition_key = "bufferdata", row_key = container_table_queue_name,
                                       items_to_pop_from_queue = items_to_pop_from_queue, visibility_timeout = visibility_timeout )
        self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebqueuepreference", row = row )

    def add_url_to_queue(self, url):

        # 1. Get compatible name
        container_table_queue_name = CorgiNameGenerator.get_storage_compatible_name( url )

        # 2. Get or Create Table/Queue/Container areas for new url
        self.cloud_direct_operations.create_and_get_table( container_table_queue_name )
        self.cloud_direct_operations.create_and_get_queue( container_table_queue_name )
        self.cloud_direct_operations.create_and_get_container( container_table_queue_name )

        # 3. Add message to Queue Preference Table
        self.add_domain_to_queue_preference_table(container_table_queue_name=container_table_queue_name, items_to_pop_from_queue=1, visibility_timeout=5 * 60 * 60)

        # 4. Add message to dedicated Queue
        message = CorgiWebMessageSchemaVersion1( toVisitUrl = url, originalDomain = url, originalUrl = url,
                                                 partitionKey = url, rowKey = "%F", metadata = None )
        self.cloud_direct_operations.upsert_to_queue( queue_name = container_table_queue_name,
                                                      message = message.to_json(), visibility_timeout = 0,
                                                      time_to_live = None )
        self.cloud_direct_operations.upsert_to_queue( queue_name = "corgiweb", message = message.to_json(),
                                                      visibility_timeout = 0, time_to_live = None )

    def list_containers(self, ):
        return self.cloud_direct_operations.list_containers()

    def list_queues(self, ):
        return self.cloud_direct_operations.list_queues()

    def list_tables(self, ):
        return self.cloud_direct_operations.list_tables()

    def get_messages_from_queue(self, queue_name, buffer_size, visibility_timeout):
        return self.cloud_direct_operations.get_messages_from_queue( queue_name = queue_name,
                                                                     max_messages = buffer_size,
                                                                     visibility_timeout = visibility_timeout )

    def upsert_to_queue(self, queue_name, message, visibility_timeout=None, time_to_live=None):
        self.cloud_direct_operations.upsert_to_queue( queue_name = queue_name, message = message,
                                                      visibility_timeout = visibility_timeout,
                                                      time_to_live = time_to_live )

    def save_sitemaps(self, domain, sitemaps):

        if sitemaps:
            for sitemap in sitemaps:
                if sitemap:
                    entity = {
                        "PartitionKey": domain,
                        "RowKey": urllib.parse.quote_plus( sitemap ),
                        "Sitemap": sitemap
                    }
                    self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebsitemaps", row = entity )

    def save_robots_txt_blobs(self, data, blob_name):
        self.upload_to_blob(data, "corgirobotscache", CorgiNameGenerator.get_storage_compatible_name(blob_name))

    def update_visit_rate(self, domain, rate):

        if rate:
            partition_key = "RateLimit"
            row_key = domain

            entity = {
                "PartitionKey": partition_key,
                "RowKey": row_key,
                "ThrottlingLimitSeconds": int( rate )
            }

            self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebthrottling", row = entity )

    def can_process_domain(self, domain):

        entity = self.cloud_direct_operations.get_entity_from_table( table_name = "corgiwebthrottling",
                                                                     partition_key = "RateLimit", row_key = domain )
        if entity:
            last_access_time = entity._metadata[ 'timestamp' ].replace( tzinfo = None )

            if (datetime.datetime.utcnow() - last_access_time) < timedelta(
                    seconds = entity[ 'ThrottlingLimitSeconds' ] ):
                print( f"Not Allowed to visit {domain}" )
                return False
        else:
            entity = {
                "PartitionKey": "RateLimit",
                "RowKey": domain,
                "ThrottlingLimitSeconds": 1
            }
            self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebthrottling", row = entity )

        return True

    def visit_domain(self, domain):
        entity = {
            "PartitionKey": "RateLimit",
            "RowKey": domain,
            "ThrottlingLimitSeconds": 1
        }

        self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebthrottling", row = entity )

    def log_request(self, domain, url, status_code):
        utc_now = datetime.datetime.utcnow()
        row_key = utc_now.strftime( '%Y%m%dT%H%M%SZ' )

        entity = {
            "PartitionKey": domain,
            "RowKey": row_key,
            "Url": url,
            "StatusCode": status_code
        }

        self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebrequestslog", row = entity )

    def upload_to_blob(self, data, container_name, blob_name, metadata=None, container_suffix = ""):
        container_name = CorgiNameGenerator.get_container_compatible_name(CorgiNameGenerator.get_storage_compatible_name( container_name ) + container_suffix)
        blob_name = CorgiNameGenerator.generate_blob_name( blob_name )
        print( f"     CloudIntegration: upload_to_blob container_name {container_name}, blob_name:{blob_name}" )

        self.cloud_direct_operations.upload_blob_to_container( container_name = container_name, blob_name = blob_name,
                                                               data = data, metadata = metadata )

    def upsert_url_info_to_table(self, table_name, entity, enable_increase_visited=False, del_father_url=False):

        # 1. update entity input
        entity_dict = entity if isinstance( entity, dict ) else entity.to_dict()
        if del_father_url: entity_dict.pop( 'FatherUrl', None )

        # 2. review if entity exists
        retrieved_entity = self.cloud_direct_operations.get_entity_from_table( table_name = entity_dict[ "TableName" ],
                                                                               partition_key = entity_dict[
                                                                                   "PartitionKey" ],
                                                                               row_key = entity_dict[ "RowKey" ] )

        # 3.
        if enable_increase_visited:
            if retrieved_entity:
                # 3a.- if exists update it's visited count
                entity_dict[ 'visitedCount' ] = retrieved_entity.get( 'visitedCount', 0 ) + 1
            else:
                # 3b.- if not exists initialize at 1
                entity_dict[ 'visitedCount' ] = 1

        # 4. upsert values
        self.cloud_direct_operations.upsert_to_table( table_name = entity_dict[ "TableName" ], row = entity_dict )

        # 5. return if value existed already
        return retrieved_entity is not None

    def delete_message_from_queue(self, queue_name, message):
        self.cloud_direct_operations.delete_message_from_queue( queue_name = queue_name, message = message )

    def list_blobs_in_container_n(self, container_name, n):
        return self.cloud_direct_operations.list_blob_names_from_container( container_name = container_name, max_results = n )

    def get_entities_from_table(self, table_name):
        return self.cloud_direct_operations.get_entities_from_table( table_name = table_name )

    def get_blob_properties(self, container_name, blob_name):
        return self.cloud_direct_operations.get_blob_properties( container_name = container_name,
                                                                 blob_name = blob_name )

    def get_blob_text(self, container_name, blob_name):
        return self.cloud_direct_operations.get_blob_text( container_name = container_name, blob_name = blob_name )

    def delete_blob_from_container(self, container_name, blob_name):
        return self.cloud_direct_operations.delete_blob_from_container( container_name = container_name,
                                                                        blob_name = blob_name )

    def get_entity_from_table(self, table_name, partition_key, row_key):
        return self.cloud_direct_operations.get_entity_from_table( table_name = table_name, partition_key = partition_key, row_key = row_key )

    def add_url_to_hash_table(self, new_url ):
        row = CorgiHashTable(new_url)
        self.cloud_direct_operations.upsert_to_table( table_name = "corgiwebhashtable", row = row )

    def retrieve_hash_for_partitions(self, partitions, max_value):
        """
        Retrieves row keys from specified partitions, respecting a maximum limit.

        Parameters:
        - partitions (list of str): List of partition keys to query for.
        - max_value (int): The maximum total number of row keys to retrieve across all partitions.

        Returns:
        - list: A list of row keys, limited by max_value.
        """
        all_row_keys = set()
        for partition_key in partitions:
            remaining_quota = max_value - len(all_row_keys)
            if remaining_quota <= 0:
                break  # Stop if the maximum number of row keys has been reached

            partition_row_keys = self.cloud_direct_operations.list_row_keys_from_partition(partition_key, max_value=remaining_quota)
            all_row_keys.update(partition_row_keys)

        return all_row_keys

