import os
import json
from pathlib import Path

class SettingsManager:

    def __init__(self,):
        self.settings = {}
        self.load_cloud_settings()
        self.load_crawler_settings()
        self.load_scraper_settings()

    def load_cloud_settings(self,):

        self.settings["CLOUD"] = {
            "AZURE_STORAGE_ACCOUNT_NAME": "",
            "AZURE_STORAGE_ACCOUNT_KEY": "",
            "USE_AZURE_STORAGE_ACCOUNT_KEY": True,
            "ENABLE_LOGS_azure_integration": False
        }

    def load_crawler_settings(self,):

        self.settings["CRAWLER"] = {
            "ADD_NEW_URLS_TO_TABLE": True,
            "ADD_NEW_URLS_TO_QUEUE": True,
            "PROCESS_VISITED_URL": True,
            "CRAWLER_SLEEP_IN_SECONDS": 20,
            "QUEUE_ONLY_DOMAINS": [],
            "CRAWLER_CYCLES_COUNT" : 1000000,
            "ENABLE_CORGIWEB_QUEUE": True,
            "CORGIWEB_QUEUE_ITEMS_TO_POP": 30,
            "CRAWLER_URLS_TO_VISIT": 1000000,
            "HTTP_PROVIDER":"aiohttp"
        }

    def load_scraper_settings(self,):

        self.settings["SCRAPER"] = {
            "H1_LIMIT" : 500,
            "MAX_IMAGES" : 10,
            "MAX_PARAGRAPH_LENGTH" : 1000,
            "MAX_LINKS" : 10000,
            "ONLY_DOMAINS": [],
            "SCRAPE_SLEEP_IN_SECONDS": 30,
            "MAX_BLOBS_PER_BATCH": 1000,
            "SCRAPER_CYCLES_COUNT": 100000,
            "ALLOW_ONLY_NEW_URLS_SAME_SITE": True,
            "HASH_PARTITIONS": [],
            "HASH_MAX_COUNT": 1000000
        }

    def __getattr__(self, item):
        try:
            return self.settings[ item ]
        except KeyError:
            raise AttributeError( f"Setting '{item}' not found" )