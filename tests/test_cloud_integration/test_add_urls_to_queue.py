import os
import unittest
import json
from dotenv import load_dotenv

import json

from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_settings.SettingsManager import SettingsManager


class TestDemo(unittest.TestCase):

    def initialize(self,):
        # Load the JSON data from the file
        settings_manager = SettingsManager()
        load_dotenv()
        settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_NAME" ] = os.getenv( "AZURE_STORAGE_ACCOUNT_NAME" )
        settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_KEY" ] = os.getenv( "AZURE_STORAGE_ACCOUNT_KEY" )
        self.assertEqual( settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_NAME" ], 'testaccountcorgibrowser' )
        self.cloud_integration = CloudIntegration( settings_manager = settings_manager )
        self.cloud_integration.initialize()

    def test_initialize(self):
        self.initialize()
        self.assertIsNotNone(self.cloud_integration)

    def test_add_urls_to_search(self):
        self.initialize()
        self.cloud_integration.add_url_to_queue("https://eluniversal.com/")

        containers = self.cloud_integration.list_containers()
        queues = self.cloud_integration.list_queues()
        tables = self.cloud_integration.list_tables()

        # test website tables/queues/tables
        self.assertTrue( "eluniversalcom" in containers )
        self.assertTrue( "eluniversalcom" in queues )
        self.assertTrue( "eluniversalcom" in tables )

        # test system tables/queues/tables
        self.assertTrue( "corgiweb" in queues )
        self.assertTrue( "corgiwebqueuepreference" in tables )
        self.assertTrue( "corgiwebrequestslog" in tables )
        self.assertTrue( "corgiwebsitemaps" in tables )
        self.assertTrue( "corgiwebthrottling" in tables )

        eluniversalcom_messages = self.cloud_integration.get_messages_from_queue("eluniversalcom",1,1)

        for msg in [eluniversalcom_messages]:

            content_str = msg[ 0 ][ 'content' ]
            data = json.loads( content_str )

            self.assertTrue(data["toVisitUrl"] == "https://eluniversal.com/")
            self.assertTrue( data[ "version" ] == 1)
            self.assertTrue( data[ "originalDomain" ] == "https://eluniversal.com/")
            self.assertTrue( data[ "originalUrl" ] == "https://eluniversal.com/")
            self.assertTrue( data[ "partitionKey" ]  == "https://eluniversal.com/" )
            self.assertTrue( data[ "rowKey" ] == "%F")
            self.assertTrue( data[ "metadata" ] == {} )
            self.assertTrue( data[ "status" ] == 'pending')

        # Test Queue Preference
        entity = self.cloud_integration.get_entity_from_table( "corgiwebqueuepreference", "bufferdata", "eluniversalcom" )
        self.assertTrue(entity[ 'ItemsToPopFromQueue' ] == 1)
        self.assertTrue(entity[ 'VisibilityTimeout' ] == 18000)







