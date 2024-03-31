import os
from dotenv import load_dotenv
from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_datasets.DataSetsManager import DataSetsManager
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_crawler.crawler import *

# Load Settings Manager
settings_manager = SettingsManager()
load_dotenv()
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT")
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT")

# Set Up cloud
CloudIntegration(settings_manager = settings_manager)
cloud_integration = CloudIntegration( settings_manager = settings_manager )
cloud_integration.initialize()

# Add Initial URLs
for url in DataSetsManager.load_usa_newspaper_urls():
    cloud_integration.add_url_to_queue(url)

# Crawl
crawler = WebCrawler(cloud_integration = cloud_integration, settings_manager=settings_manager )
crawler.initialize()
crawler.start()
