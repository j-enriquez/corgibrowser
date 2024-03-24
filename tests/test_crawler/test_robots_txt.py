import os
import unittest
import json
from dotenv import load_dotenv

import json

from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_crawler.crawler import WebCrawler
from corgibrowser.corgi_settings.SettingsManager import SettingsManager


class TestRobotsTxt(unittest.TestCase):

    def initialize(self,):
        # Load the JSON data from the file
        self.settings_manager = SettingsManager()
        load_dotenv()
        self.settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_NAME" ] = os.getenv( "AZURE_STORAGE_ACCOUNT_NAME" )
        self.settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_KEY" ] = os.getenv( "AZURE_STORAGE_ACCOUNT_KEY" )
        self.assertEqual( self.settings_manager.CLOUD[ "AZURE_STORAGE_ACCOUNT_NAME" ], 'testaccountcorgibrowser' )
        self.cloud_integration = CloudIntegration( settings_manager = self.settings_manager )
        self.cloud_integration.initialize()

    def test_robots_txt_is_downloaded(self):
        self.initialize()

        new_urls = [
            "https://abcnews.go.com/"
        ]
        for url in new_urls:
            self.cloud_integration.add_url_to_queue(url)

        self.settings_manager.CRAWLER[ "CRAWLER_CYCLES_COUNT" ] = 1
        self.settings_manager.CRAWLER[ "CRAWLER_SLEEP_IN_SECONDS" ] = 0
        self.settings_manager.CRAWLER[ "CRAWLER_URLS_TO_VISIT" ] = 1
        crawler = WebCrawler( cloud_integration = self.cloud_integration,
                              settings_manager = self.settings_manager )
        crawler.initialize()
        crawler.start()

        # pending add validation for abcnewsgocom

        #Validate robots.txt
        self.assertIsNotNone(self.cloud_integration.get_blob_text("corgirobotscache", "abcnewsgocom"))










