Crawler Component Documentation
=============================================

Getting Started with the CorgiBrowser Crawler
---------------------------------------------

The CorgiBrowser framework is designed to simplify web crawling and scraping processes. This documentation focuses on the Crawler component, guiding you through initializing the crawler with Azure Cloud integration, setting up initial URLs from a predefined dataset, and starting the crawling process.

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

The `CloudIntegration` class is responsible for managing cloud-related functionalities, including connecting to Azure Storage services.

3. **Load Initial URLs**:

The `DataSetsManager` provides access to predefined datasets, such as a list of USA newspaper URLs, to populate your crawling queue with initial URLs.

Sample Code for Crawler Initialization
--------------------------------------

Below is a demo showing how to set up and start the crawler::

    import os
    from dotenv import load_dotenv
    from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
    from corgibrowser.corgi_datasets.DataSetsManager import DataSetsManager
    from corgibrowser.corgi_settings.SettingsManager import SettingsManager
    from corgibrowser.corgi_crawler.crawler import WebCrawler

    # Load Settings Manager
    settings_manager = SettingsManager()
    load_dotenv()
    settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

    # Set Up Cloud Integration
    cloud_integration = CloudIntegration(settings_manager=settings_manager)
    cloud_integration.initialize()

    # Add Initial URLs to Queue
    for url in DataSetsManager.load_usa_newspaper_urls():
        cloud_integration.add_url_to_queue(url)

    # Initialize and Start the Crawler
    crawler = WebCrawler(cloud_integration=cloud_integration, settings_manager=settings_manager)
    crawler.initialize()
    crawler.start()

Understanding the Crawler Components
------------------------------------

- **SettingsManager**: Manages all configurations and settings across the CorgiBrowser framework, including cloud storage details.

- **CloudIntegration**: Handles the integration with cloud services, enabling functionalities like URL queue management in cloud storage.

- **WebCrawler**: The core component that orchestrates the crawling process, including initializing crawls, managing crawl queues, and processing URLs based on predefined or custom logic.

Advanced Configuration and Usage
--------------------------------

For advanced users looking to customize the crawling process, the CorgiBrowser framework offers extendable classes and methods allowing for tailored crawling strategies, including handling of `robots.txt` for ethical crawling practices and processing of visited URLs.

Refer to the framework's GitHub repository for more examples and advanced configuration options.
