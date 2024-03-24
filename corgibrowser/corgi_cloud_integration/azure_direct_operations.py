import datetime

from azure.core.exceptions import ResourceExistsError, HttpResponseError, ResourceNotFoundError
from azure.data.tables import TableServiceClient, UpdateMode
from azure.storage.queue import QueueServiceClient
from azure.storage.blob import BlobServiceClient


class AzureDirectOperations:
    def __init__(self, config):
        self.config = config

        # clients
        self.table_service_client = None
        self.queue_service_client = None
        self.blob_service_client = None

        # Initialize caches for created resources
        self.created_tables = set()
        self.created_queues = set()
        self.created_containers = set()

        self.last_refresh = None
        self.refresh_credentials()

    def refresh_credentials(self):

        refresh_interval = datetime.timedelta( minutes = 5 )
        if self.last_refresh:
            if datetime.datetime.now() - self.last_refresh > refresh_interval:
                self.last_refresh = datetime.datetime.now()
            else:
                return
        else:
            self.last_refresh = datetime.datetime.now()

        if self.config[ 'USE_AZURE_STORAGE_ACCOUNT_KEY' ]:
            storage_account_name = self.config[ 'AZURE_STORAGE_ACCOUNT_NAME' ]
            storage_account_key = self.config[ 'AZURE_STORAGE_ACCOUNT_KEY' ]

            connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

            self.blob_service_client = BlobServiceClient.from_connection_string( connection_string )
            self.table_service_client = TableServiceClient.from_connection_string( connection_string )
            self.queue_service_client = QueueServiceClient.from_connection_string( connection_string )
        else:
            raise

        self.last_refresh = datetime.datetime.now()


    def upsert_to_queue(self, queue_name, message, visibility_timeout=0, time_to_live=None ):
        # Ensure the queue exists and get the queue client
        queue_client = self.create_and_get_queue( queue_name )

        # Serialize the message if it's not already a string (assuming it's a dict)
        if isinstance( message, dict ):
            import json
            message = json.dumps( message )

        try:
            # Add the message to the queue
            queue_client.send_message( message, visibility_timeout = visibility_timeout, time_to_live = time_to_live )
            print( f"Message upserted to queue '{queue_name}'." )
        except Exception as e:
            print( f"Failed to upsert message to queue '{queue_name}': {e}" )
            raise e

    def upsert_to_table(self, table_name, row):
        self.refresh_credentials()

        # Ensure the table exists and get the table client
        table_client = self.create_and_get_table( table_name )

        # Check if 'row' is already a dict, if not, convert it using 'to_dict()' method
        row_dict = row if isinstance( row, dict ) else row.to_dict()

        try:
            # Upsert the entity to the table. Default mode is Merge, which updates an existing entity or inserts a new one.
            # If the entity does not exist, it will be inserted. If it does exist, its properties will be merged with the provided entity.
            table_client.upsert_entity( entity = row_dict, mode = UpdateMode.MERGE )
            print( f"Entity upserted to table '{table_name}'." )
        except Exception as e:
            print( f"Failed to upsert entity to table '{table_name}': {e}" )
            raise e

    def create_and_get_table(self, table_name):
        self.refresh_credentials()

        table_client = self.table_service_client.get_table_client(table_name=table_name)
        if table_name not in self.created_tables:
            try:
                table_client.create_table()
                print(f"Table '{table_name}' created.")
            except HttpResponseError as e:
                if e.status_code != 409:  # 409 Conflict indicates table already exists
                    raise
                else:
                    print(f"Table '{table_name}' already exists. Skipping creation.")
            self.created_tables.add(table_name)
        else:
            print(f"Table '{table_name}' is already created. Skipping creation.")
        return table_client

    def create_and_get_queue(self, queue_name):
        self.refresh_credentials()

        queue_client = self.queue_service_client.get_queue_client(queue=queue_name)
        if queue_name not in self.created_queues:
            try:
                queue_client.create_queue()
                print(f"Queue '{queue_name}' created.")
            except ResourceExistsError:
                print(f"Queue '{queue_name}' already exists. Skipping creation.")
            except Exception as e:
                raise e
            self.created_queues.add(queue_name)
        else:
            print(f"Queue '{queue_name}' is already created. Skipping creation.")
        return queue_client

    def create_and_get_container(self, container_name):
        self.refresh_credentials()

        container_client = self.blob_service_client.get_container_client(container=container_name)
        if container_name not in self.created_containers:
            try:
                container_client.create_container()
                print(f"Container '{container_name}' created.")
            except ResourceExistsError:
                print(f"Container '{container_name}' already exists. Skipping creation.")
            except Exception as e:
                raise e
            self.created_containers.add(container_name)
        else:
            print(f"Container '{container_name}' is already created. Skipping creation.")
        return container_client

    def upload_blob_to_container(self, container_name, blob_name, data, metadata=None):
        """
        Uploads data to a blob in a specified container. If the blob already exists, it is overwritten.

        Parameters:
        - container_name (str): The name of the container to which the blob will be uploaded.
        - blob_name (str): The name of the blob.
        - data: The data to upload. Can be bytes, a string, or a file-like object.
        - metadata (dict, optional): A dictionary containing metadata to associate with the blob.

        Returns:
        - BlobClient: A BlobClient instance representing the uploaded blob.
        """
        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # Get a client for the blob
            blob_client = container_client.get_blob_client( blob_name )

            # Upload the blob
            blob_client.upload_blob( data, overwrite = True, metadata = metadata )
            print( f"Blob '{blob_name}' uploaded to container '{container_name}'." )
            return blob_client
        except Exception as e:
            print( f"Failed to upload blob '{blob_name}' to container '{container_name}': {e}" )
            raise

    def get_messages_from_queue(self, queue_name, max_messages=32, visibility_timeout=None):
        """
        Retrieves messages from the specified Azure Queue Storage queue.

        Parameters:
        - queue_name (str): The name of the queue to retrieve messages from.
        - num_messages (int): The maximum number of messages to retrieve. Default is 32.
        - visibility_timeout (int): The visibility timeout for the retrieved messages, in seconds.
                                    If None, the default visibility timeout for the queue is used.

        Returns:
        - list: A list of retrieved messages.
        """

        # Ensure the queue exists and get the queue client
        queue_client = self.create_and_get_queue( queue_name )

        try:
            # Retrieve messages from the queue
            messages = queue_client.receive_messages( max_messages = max_messages,
                                                      visibility_timeout = visibility_timeout )
            messages_list = list( messages )
            print( f"Retrieved {len( messages_list )} messages from queue '{queue_name}'." )
            return messages_list
        except Exception as e:
            print( f"Failed to retrieve messages from queue '{queue_name}': {e}" )
            raise e

    def list_containers(self):
        self.refresh_credentials()
        return [ container.name for container in self.blob_service_client.list_containers() ]

    def list_queues(self):
        self.refresh_credentials()
        return [ queue.name for queue in self.queue_service_client.list_queues() ]

    def list_tables(self):
        self.refresh_credentials()
        return [ table.name for table in self.table_service_client.list_tables() ]

    def get_entity_from_table(self, table_name, partition_key, row_key):
        """
        Retrieves an entity from the specified Azure Table Storage table.

        Parameters:
        - table_name (str): The name of the table to retrieve the entity from.
        - partition_key (str): The partition key of the entity.
        - row_key (str): The row key of the entity.

        Returns:
        - dict: The entity if found.
        - None: If the entity does not exist.
        """
        self.refresh_credentials()

        # Ensure the table exists and get the table client
        table_client = self.create_and_get_table( table_name )

        try:
            # Attempt to retrieve the entity
            entity = table_client.get_entity( partition_key = partition_key, row_key = row_key )
            return entity
        except ResourceNotFoundError:
            # Entity not found
            print(
                f"Entity with PartitionKey '{partition_key}' and RowKey '{row_key}' not found in table '{table_name}'." )
            return None
        except Exception as e:
            # Handle other exceptions
            print( f"Failed to retrieve entity from table '{table_name}': {e}" )
            raise

    def get_entities_from_table(self, table_name):
        """
        Retrieves entities from the specified Azure Table Storage table.

        Parameters:
        - table_name (str): The name of the table to retrieve entities from.
        - query_filter (str): An OData filter expression that specifies the subset of entities to retrieve.
                              Default is None, which means all entities are retrieved.

        Returns:
        - list: A list of dictionaries, where each dictionary represents an entity.
        """
        self.refresh_credentials()

        # Ensure the table exists and get the table client
        table_client = self.create_and_get_table( table_name )

        try:
            entities = table_client.list_entities()
            entities_list = [ entity for entity in entities ]
            print( f"Retrieved {len( entities_list )} entities from table '{table_name}'." )
            return entities_list
        except Exception as e:
            print( f"Failed to retrieve entities from table '{table_name}': {e}" )
            raise e

    def list_blobs_from_container(self, container_name):
        """
        Retrieves blobs from the specified Azure Blob Storage container.

        Parameters:
        - container_name (str): The name of the container to retrieve blobs from.

        Returns:
        - list: A list of blob objects, where each object represents a blob in the container.
        """
        self.refresh_credentials()

        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # List all blobs in the container
            blob_items = container_client.list_blobs()
            blobs_list = [ blob for blob in blob_items ]
            print( f"Retrieved {len( blobs_list )} blobs from container '{container_name}'." )
            return blobs_list
        except Exception as e:
            print( f"Failed to retrieve blobs from container '{container_name}': {e}" )
            raise e

    def list_blob_names_from_container(self, container_name, max_results=None):
        """
        Retrieves the names of blobs from the specified Azure Blob Storage container, up to a specified maximum number of blobs.

        Parameters:
        - container_name (str): The name of the container to retrieve blob names from.
        - max_results (int, optional): The maximum number of blob names to retrieve. If None, all blob names are retrieved.

        Returns:
        - list: A list of strings, where each string represents the name of a blob in the container.
        """
        self.refresh_credentials()

        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # Use the 'list_blob_names' method with 'results_per_page' to limit the number of retrieved blob names
            blob_names = container_client.list_blob_names( results_per_page = max_results )
            blob_names_list = list( blob_names )
            print( f"Retrieved {len( blob_names_list )} blob names from container '{container_name}'." )
            return blob_names_list
        except Exception as e:
            print( f"Failed to retrieve blob names from container '{container_name}': {e}" )
            raise e

    def delete_message_from_queue(self, queue_name, message):
        """
        Deletes a specific message from the specified Azure Queue Storage queue.

        Parameters:
        - queue_name (str): The name of the queue from which to delete the message.
        - message: The message object to be deleted, which must have 'id' and 'pop_receipt' attributes.
        """
        print( f"Deleting message: Type: {type( message )}, Content: {message}" )

        try:
            # Ensure the queue exists and get the queue client
            queue_client = self.create_and_get_queue( queue_name )

            # Delete the specified message from the queue
            queue_client.delete_message( message.id, message.pop_receipt )
            print( f"Message successfully deleted from queue '{queue_name}'." )
        except Exception as e:
            print( f"Error deleting message from queue '{queue_name}': {e}" )
            raise

    def get_blob_properties(self, container_name, blob_name):
        """
        Retrieves properties of a blob within a specified container.

        Parameters:
        - container_name (str): The name of the container containing the blob.
        - blob_name (str): The name of the blob whose properties are to be retrieved.

        Returns:
        - dict: A dictionary containing the blob's properties.
        """
        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # Get a client for the blob
            blob_client = container_client.get_blob_client( blob_name )

            # Retrieve the blob's properties
            blob_properties = blob_client.get_blob_properties()
            print( f"Properties for blob '{blob_name}' in container '{container_name}' retrieved successfully." )

            # Optionally, you might want to convert the properties to a dictionary or another format
            # depending on how you plan to use them. For simplicity, this example returns the properties object.
            return blob_properties
        except Exception as e:
            print( f"Failed to retrieve properties for blob '{blob_name}' in container '{container_name}': {e}" )
            return None

    def get_blob_text(self, container_name, blob_name):
        """
        Retrieves the text content of a blob in a specified container.

        Parameters:
        - container_name (str): The name of the container from which the blob will be retrieved.
        - blob_name (str): The name of the blob to retrieve.

        Returns:
        - str: The text content of the blob.
        """
        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # Get a client for the blob
            blob_client = container_client.get_blob_client( blob_name )

            # Download the blob's content and return as text
            blob_text = blob_client.download_blob().content_as_text()
            print( f"Blob '{blob_name}' content retrieved from container '{container_name}'." )
            return blob_text
        except Exception as e:
            print( f"Failed to retrieve blob '{blob_name}' content from container '{container_name}': {e}" )
            return None

    def delete_blob_from_container(self, container_name, blob_name):
        """
        Deletes a blob from a specified container.

        Parameters:
        - container_name (str): The name of the container from which the blob will be deleted.
        - blob_name (str): The name of the blob to delete.

        Returns:
        - bool: True if the blob was successfully deleted, False otherwise.
        """
        # Ensure the container exists and get the container client
        container_client = self.create_and_get_container( container_name )

        try:
            # Get a client for the blob
            blob_client = container_client.get_blob_client( blob_name )

            # Delete the blob
            blob_client.delete_blob()
            print( f"Blob '{blob_name}' successfully deleted from container '{container_name}'." )
            return True
        except Exception as e:
            print( f"Failed to delete blob '{blob_name}' from container '{container_name}': {e}" )
            return False

    def list_row_keys_from_partition(self, partition_key, max_value=None):
        """
        Iterates over all entities in a given partition and collects their row keys.
        Designed to efficiently handle large datasets.

        Parameters:
        - partition_key (str): The partition key to query for.

        Returns:
        - list: A list of row keys from the specified partition.
        """
        table_client = self.create_and_get_table("corgiwebhashtable")

        row_keys = set()
        query_filter = f"PartitionKey eq '{partition_key}'"

        # The query_entities method returns an ItemPaged object that supports lazy loading.
        # Entities are fetched in pages as you iterate over the collection, making this efficient for large datasets.
        entities = table_client.query_entities( query_filter = query_filter, select = [ 'RowKey' ] )

        for entity in entities:
            if max_value is not None and len( row_keys ) >= max_value:
                break  # Stop collecting keys if the max_value limit is reached
            row_keys.add( entity[ 'RowKey' ] )

        return row_keys