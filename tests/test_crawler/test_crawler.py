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




