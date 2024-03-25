import os
import unittest

from dotenv import load_dotenv

import json

from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_crawler.crawler import WebCrawler
from corgibrowser.corgi_settings.SettingsManager import SettingsManager


class TestCrawler(unittest.TestCase):

    def test_initialize_crawler(self):
        # Load the JSON data from the file
        settings_manager = SettingsManager()
        load_dotenv()
        settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        cloud_integration = CloudIntegration(settings_manager = settings_manager)
        cloud_integration.initialize()

        settings_manager.CRAWLER["CRAWLER_CYCLES_COUNT"] = 1
        settings_manager.CRAWLER[ "CRAWLER_SLEEP_IN_SECONDS" ] = 0
        settings_manager.CRAWLER[ "CRAWLER_URLS_TO_VISIT" ] = 1
        crawler = WebCrawler( cloud_integration = cloud_integration,
                              settings_manager = settings_manager )
        crawler.initialize()
        crawler.start()

    def test_round_robin_distribution(self):
        # Mock input simulating messages from different queues
        queue_preferences = [
            {"QueueName": "Q1", "Messages": [ {"id": 1}, {"id": 2}, {"id": 3} ]},
            {"QueueName": "Q2", "Messages": [ {"id": 4}, {"id": 5}, {"id": 6} ]},
            {"QueueName": "Q3", "Messages": [ {"id": 7}, {"id": 8} ]}
        ]

        # Simulate fetching and collecting all messages
        all_messages = [ ]
        for queue_pref in queue_preferences:
            queue_name = queue_pref[ "QueueName" ]
            for msg in queue_pref[ "Messages" ]:
                msg[ "QueueName" ] = queue_name  # Add QueueName to each message
                all_messages.append( msg )

        # Distribute messages in round-robin order
        distributed_messages = WebCrawler.distribute_round_robin( all_messages )

        # Verify round-robin distribution
        expected_queue_order = [ "Q1", "Q2", "Q3", "Q1", "Q2", "Q3", "Q1", "Q2" ]
        actual_queue_order = [ msg[ "QueueName" ] for msg in distributed_messages ]

        self.assertEqual( expected_queue_order, actual_queue_order, "Messages were not distributed in round-robin order" )


