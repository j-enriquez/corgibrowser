
class DataAnalytics:
    def __init__(self, cloud_integration,data_settings):
        self.cloud_integration = cloud_integration
        self.data_settings = data_settings

    def get_storage_account_stadistics(self):
        self.cloud_integration.list_queues_and_messages()
        # self.cloud_integration.list_tables_and_entities()
        None

        # self.check_if_needs_refresh()
        #
        # print( "\nTables and number of entities:" )
        # table_list = self.table_service_client.list_tables()
        #
        # # Initialize the table client for corgiweb_storage_analytics
        # analytics_table_client = self.table_service_client.get_table_client( "corgiwebstorageanalytics" )
        #
        # try:
        #     analytics_table_client.create_table()
        # except ResourceExistsError:
        #     pass  # Table already exists, no action needed
        #
        # for table in table_list:
        #     table_client = self.table_service_client.get_table_client( table.name )
        #     entities = list( table_client.list_entities() )
        #
        #     status_count = {}
        #     for entity in entities:
        #         # Initialize status count if not present
        #         if "Status" in entity.keys():
        #             status = entity[ "Status" ]
        #             if status not in status_count:
        #                 status_count[ status ] = 0
        #             status_count[ status ] += 1
        #
        #     print( f"Table: {table.name}, Entities: {len( entities )}" )
        #
        #     for status, count in status_count.items():
        #         # Assuming CorgiWebStorageAnalytics is properly defined and has a method to_dict()
        #         entity_CorgiWebStorageAnalytics = CorgiWebStorageAnalytics(
        #             partition_key = table.name,
        #             object_type = "Table",
        #             object_name = "CorgiWebStorageAnalytics",
        #             status = status,
        #             count = count
        #         )
        #
        #         try:
        #             entity_dict = entity_CorgiWebStorageAnalytics.to_dict()
        #             analytics_table_client.upsert_entity( entity = entity_dict, mode = UpdateMode.MERGE )
        #         except Exception as e:
        #             logging.error( f"Error upserting to table: {e}" )
        #             raise

        # def list_queues_and_messages(self, ):
        #     self.check_if_needs_refresh()
        #
        #     print( "\nQueues and number of messages:" )
        #     queue_list = self.queue_service_client.list_queues()
        #
        #     # Ensure the analytics table client is initialized once
        #     analytics_table_client = self.table_service_client.get_table_client( "corgiwebstorageanalytics" )
        #     try:
        #         analytics_table_client.create_table()
        #     except ResourceExistsError:
        #         pass  # Table already exists, no action needed
        #
        #     for queue in queue_list:
        #         queue_client = self.queue_service_client.get_queue_client( queue.name )
        #         properties = queue_client.get_queue_properties()
        #         message_count = properties.approximate_message_count
        #         print( f"Queue: {queue.name}, Messages: {message_count}" )
        #
        #         # Prepare the entity for the analytics table
        #         # Assuming CorgiWebStorageAnalytics is properly defined and has a method to_dict()
        #         entity_CorgiWebStorageAnalytics = CorgiWebStorageAnalytics(
        #             partition_key = queue.name,
        #             object_type = "Queue",
        #             object_name = "CorgiWebStorageAnalytics",
        #             status = "message_count",
        #             count = message_count
        #         )
        #
        #         try:
        #             entity_dict = entity_CorgiWebStorageAnalytics.to_dict()
        #             analytics_table_client.upsert_entity( entity = entity_dict, mode = UpdateMode.MERGE )
        #         except Exception as e:
        #             logging.error( f"Error upserting to analytics table: {e}" )
        #             raise

    def get_storage_table_data(self,table_name):
        return self.cloud_integration.get_entities_from_table("wwweluniversalcommx")
