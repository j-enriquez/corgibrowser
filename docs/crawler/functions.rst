WebCrawler Class
================

class WebCrawler(cloud_integration, settings_manager=None)[source]
------------------------------------------------------------------

A flexible and efficient web crawler designed for scalable web crawling projects.

This class orchestrates the crawling process, managing crawl queues, and processing URLs based on predefined or custom logic.

Parameters
----------
**cloud_integration** (*CloudIntegration*)
    An instance of the CloudIntegration class for managing cloud-related functionalities.

**settings_manager** (*SettingsManager*, optional)
    An instance of the SettingsManager class for managing configurations and settings. Defaults to None.

Methods
-------

**initialize()**
    Prepares the WebCrawler for operation by setting up necessary configurations and ensuring all systems are ready for the crawling process.

**start()**
    Launches the crawling process, orchestrating the crawl operations based on the configured settings.


SettingsManager Class
------------------------------

Handles the configurations and settings for the CorgiBrowser framework, including cloud storage details and crawler settings.

Methods
-------

**load_crawler_settings()**


**Modifying Crawler Settings**
------------------------------
Loads the crawler's operational settings, providing control over various aspects of the crawling process.
To update crawler settings, access and modify the `CRAWLER` dictionary through the `settings_manager` instance. For example, to change the sleep duration between crawl cycles::

    settings_manager.CRAWLER["CRAWLER_SLEEP_IN_SECONDS"] = 30

Settings Details
----------------
- **PROCESS_VISITED_URL** (*bool*): Whether to process visited URLs. Default is True.
- **CRAWLER_SLEEP_IN_SECONDS** (*int*): The sleep duration in seconds between crawl cycles. Default is 20.
- **QUEUE_ONLY_DOMAINS** (*list*): A list of domains to exclusively crawl. Defaults to an empty list.
- **CRAWLER_CYCLES_COUNT** (*int*): The number of crawler cycles to execute. Default is 1000000.
- **ENABLE_CORGIWEB_QUEUE** (*bool*): Whether to enable CorgiWeb queue management. Default is True.
- **CORGIWEB_QUEUE_ITEMS_TO_POP** (*int*): The number of items to pop from the queue. Default is 30.
- **CRAWLER_URLS_TO_VISIT** (*int*): The total number of URLs to visit. Default is 1000000.
- **HTTP_PROVIDER** (*str*): The HTTP provider to use. Default is "aiohttp".