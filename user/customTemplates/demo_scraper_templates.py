import os
from dotenv import load_dotenv
from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_webscraping.scraper import Scraper
from user.customTemplates.scraping_templates.abcnewsgocom import abcnewsgocom
from user.customTemplates.scraping_templates.fbrefcom import fbrefcom
from user.customTemplates.scraping_templates.wwwcnncom import wwwcnncom
from user.customTemplates.scraping_templates.wwweluniversalcommx import wwweluniversalcommx

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
settings_manager.SCRAPER["ONLY_DOMAINS"] = [
    "fbrefcom",
    "wwweluniversalcommx",
    "abcnewsgocom",
    "wwwcnncom"]
settings_manager.SCRAPER["HASH_PARTITIONS"] = [
    "fbrefcom",
    "wwweluniversalcommx",
    "abcnewsgocom",
    "wwwcnncom"]
scraper_dict = scraper_dict = {
    "fbrefcom": fbrefcom,
    "wwweluniversalcommx": wwweluniversalcommx,
    "abcnewsgocom": abcnewsgocom,
    "wwwcnncom": wwwcnncom
}
scraper = Scraper(cloud_integration = cloud_integration, settings_manager=settings_manager, scraper_dict=scraper_dict )
scraper.initialize()
scraper.start()
