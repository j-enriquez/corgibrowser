Scraper Component Documentation
=============================================

Getting Started with the CorgiBrowser Scraper
---------------------------------------------

This section of the documentation focuses on the `Scraper` component, which is designed to extract specific data from web pages that have been identified by the crawler. Follow these steps to initialize the scraper with Azure Cloud integration and start the scraping process.

Prerequisites
-------------

- Python 3.9+
- `An active Azure Storage Account <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal>`_
- The CorgiBrowser framework installed in your environment


Installation
------------

Ensure you have CorgiBrowser installed. If not, you can install it using pip::

    pip install corgibrowser

Configuration
-------------

1. **Environment Setup**: Start by setting up your environment variables. You need to have `AZURE_STORAGE_ACCOUNT_NAME` and `AZURE_STORAGE_ACCOUNT_KEY` defined in your `.env` file to authenticate with Azure Storage. `Get Azure Storage Keys <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal>`_

    **.env file example**::

        AZURE_STORAGE_ACCOUNT_NAME=<REPLACE_WITH_ACCOUNT_NAME>
        AZURE_STORAGE_ACCOUNT_KEY=<REPLACE_WITH_ACCOUNT_KEY>

2. **Initialize the Cloud Integration**:

The `CloudIntegration` class manages the interaction with cloud services, allowing to connect with Azure Storage facilities.

Sample Code for Scraper Initialization
--------------------------------------

The following example demonstrates how to configure and initiate the scraper::

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

    # Set Up Cloud Integration
    cloud_integration = CloudIntegration(settings_manager=settings_manager)
    cloud_integration.initialize()

    # Initialize and Start the Scraper
    scraper = Scraper(cloud_integration=cloud_integration, settings_manager=settings_manager)
    scraper.initialize()
    scraper.start()

Understanding the Scraper Components
-------------------------------------

- **SettingsManager**: Centralizes configuration management, including details for cloud storage access.

- **CloudIntegration**: Facilitates cloud service integration.

- **Scraper**: The main component responsible for the data extraction process, allowing predefined or custom scraping templates for targeted data retrieval.

Advanced Configuration and Usage
--------------------------------

The `CorgiBrowser` framework is built to accommodate customization, offering users the ability to define specific scraping logic, manage `robots.txt` compliance, and process large volumes of data efficiently.

Refer to the GitHub repository for detailed examples, advanced configurations, and additional scraping templates.


Scraper with templates and HashPartition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example demonstrates how to configure and initiate the scraper::

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

    # Scrape limiting to certain domains
    settings_manager.SCRAPER["ONLY_DOMAINS"] = [
        "fbrefcom",
        "wwweluniversalcommx",
        "abcnewsgocom",
        "wwwcnncom"]

    # Download the Hash table for the following domains, to have visited urls in memory
    settings_manager.SCRAPER["HASH_PARTITIONS"] = [
        "fbrefcom",
        "wwweluniversalcommx",
        "abcnewsgocom",
        "wwwcnncom"]

    # Custom Templates
    scraper_dict = scraper_dict = {
        "fbrefcom": fbrefcom,
        "wwweluniversalcommx": wwweluniversalcommx,
        "abcnewsgocom": abcnewsgocom,
        "wwwcnncom": wwwcnncom
    }
    scraper = Scraper(cloud_integration = cloud_integration, settings_manager=settings_manager, scraper_dict=scraper_dict )
    scraper.initialize()
    scraper.start()



Example of custom template for www.cnn.com::

    from bs4 import BeautifulSoup
    from parsel import Selector

    from corgibrowser.corgi_webscraping.default_scrape_template import ScrapingTemplate


    class wwwcnncom(ScrapingTemplate):
        def initialize(self, ):
            self.soup = BeautifulSoup( self.html_text, "lxml" )

        def extra_data(self, ):
            self.sel = Selector( text = self.html_text )
            if self.sel.xpath("//main[@class='article__main']" ):
                self.handle_article()
            else:
                self.extra_keys[ "ContainerSuffix" ] = "unknown2"
            self.extra_keys[ "html_text" ] = self.html_text


        def handle_homepage(self, ):
            self.extra_keys["ContainerSuffix"] = "homepage"
            self.extra_keys[ "images" ] = ""
            self.extra_keys[ "paragraphs" ] = ""
            self.extra_keys[ "html_text" ] = ""

        def handle_article(self, ):
            self.extra_keys[ "ContainerSuffix" ] = "article"

            self.extra_keys["h1"] = self.get_image_urls_by_xpath(self.sel,"//meta[@property='og:title']","/@content")
            self.extra_keys[ "images" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='twitter:image']","/@content")
            self.extra_keys[ "category" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='twitter:image']","/@content")

            self.extra_keys[ "author" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='author']","/@content")
            self.extra_keys[ "author_date" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@property='article:published_time']","/@content")

            article_sel = self.sel.xpath( "//div[@class='article__content']" )
            self.extra_keys[ "paragraphs" ] = self.extract_all_text(article_sel,"//p")[: 2000 ]

            self.extra_keys["SourceDataField"] = self.extra_keys[ "h1" ] + " " + self.extra_keys["paragraphs"]
            self.extra_keys["SourceDataField"] = self.extra_keys["SourceDataField"][: 2000 ]

