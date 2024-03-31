import os
from dotenv import load_dotenv
from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_webscraping.scraper import Scraper

# Load Settings Manager
settings_manager = SettingsManager()
load_dotenv()
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

# Set Up cloud
CloudIntegration(settings_manager = settings_manager)
cloud_integration = CloudIntegration( settings_manager = settings_manager )
cloud_integration.initialize()

# Scrape
scraper = Scraper(cloud_integration = cloud_integration, settings_manager=settings_manager )
scraper.initialize()
scraper.start()
