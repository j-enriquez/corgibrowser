Scraper Class
================

class Scraper(cloud_integration, settings_manager=None, scraper_dict={})[source]
--------------------------------------------------------------------------------

Scraper component within the CorgiBrowser framework for efficient data extraction from various web containers. Utilizes cloud integration for scalable processing and storage management.

Parameters
----------
**cloud_integration** (*CloudIntegration*)
    An instance of the CloudIntegration class for managing cloud-related functionalities.

**settings_manager** (*SettingsManager*, optional)
    An instance of the SettingsManager class for managing configurations and settings. Defaults to None.

**scraper_dict** (*dict*, optional)
    A dictionary containing specific scraper configurations. Defaults to an empty dict.

Methods
-------

**initialize()**
    Prepares the Scraper for operation by setting up necessary configurations and ensuring all systems are ready for the scraping process.

**start()**
    Launches the scraping process, orchestrating the data extraction operations based on the configured settings and containers to visit.


SettingsManager Component
----------------------------------------

Responsible for loading and managing the Scraper's configurations, facilitating customization of the scraping behavior.

**Modifying Scraper Settings**
--------------------------------
Loads the scraper's operational settings, providing control over various aspects of the scraping process.
To update scraper settings, access and modify the `SCRAPER` dictionary through the `settings_manager` instance. For example, to change the maximum number of images to process::

    settings_manager.SCRAPER["MAX_IMAGES"] = 20

Settings Details
----------------

Used on default Scrape Templates:

- **H1_LIMIT** (*int*): The maximum length to retrieve for H1.
- **MAX_IMAGES** (*int*): The maximum number of images to process. Default is 10.
- **MAX_PARAGRAPH_LENGTH** (*int*): The maximum length of paragraphs to process. Default is 1000.
- **MAX_LINKS** (*int*): The maximum number of links to process. Default is 10000.

Queue Related:

- **ONLY_DOMAINS** (*list*): A list of domains to exclusively scrape. Defaults to an empty list which means to take from corgiwebqueuepreference table.
- **SCRAPE_SLEEP_IN_SECONDS** (*int*): The sleep duration in seconds between scrape cycles. Default is 30.
- **MAX_BLOBS_PER_BATCH** (*int*): The maximum number of blobs to process per batch. Default is 1000.
- **SCRAPER_CYCLES_COUNT** (*int*): The number of scraper cycles to execute. Default is 100000.
- **ALLOW_ONLY_NEW_URLS_SAME_SITE** (*bool*): Whether to allow only new URLs from the same site. Default is True.
- **HASH_PARTITIONS** (*list*): A list of hash partitions for managing URL hashes. Defaults to an empty list.
- **HASH_MAX_COUNT** (*int*): The maximum count of hashes to manage. Default is 1000000.
