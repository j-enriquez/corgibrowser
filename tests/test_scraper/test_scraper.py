import os
import unittest

from dotenv import load_dotenv

import json

from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_webscraping.scraper import Scraper


class TestScraper(unittest.TestCase):

    def test_initialize_scraper(self):
        # Load the JSON data from the file
        settings_manager = SettingsManager()
        load_dotenv()
        settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        cloud_integration = CloudIntegration(settings_manager = settings_manager)
        cloud_integration.initialize()

        settings_manager.SCRAPER["SCRAPER_CYCLES_COUNT"] = 1
        settings_manager.SCRAPER[ "SCRAPE_SLEEP_IN_SECONDS" ] = 0
        settings_manager.SCRAPER[ "MAX_BLOBS_PER_BATCH" ] = 0
        cloud_integration = CloudIntegration( settings_manager = settings_manager )
        scraper = Scraper( cloud_integration = cloud_integration, settings_manager = settings_manager )
        scraper.initialize()
        scraper.start()





