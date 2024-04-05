CorgiHashTable
==================================

This table is responsible for the storage unique URLs identifying them and ensuring their uniqueness during the crawling and scraping processes.

**Note: future improvements considers move this to Redis as in-memory distributed caching**

Class Definition
----------------

.. code-block:: python

    class CorgiHashTable:
        def __init__(self, full_url):
            self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(full_url)
            self.RowKey = UrlHash.encode_url(full_url)
            self.FullUrl = full_url

        def to_dict(self):
            return {
                "PartitionKey": self.PartitionKey,
                "RowKey": self.RowKey,
                "FullUrl": self.FullUrl
            }

Utilizing SHA-256 encoding, CorgiHashTable generates a unique `RowKey` for each URL. It assigns a `PartitionKey` for database partitioning to enhance data retrieval speeds.

Scraping Process Steps
----------------------

The scraping process is structured as follows:

1. **Local Hash Cache Initialization**: Set up an in-memory list of visited URLs for quick reference.
2. **Data Retrieval from Cloud Storage**: Fetch HTML content from scalable cloud storage to minimize local resource usage.
3. **Template Matching for Data Extraction**: Align scraping activities with a schema template for structured data output.
4. **Data Storage**: Save extracted data in either a partitioned database or a specified directory.
5. **Metadata Updating**: Keep track of scraping activities through timely metadata updates.
6. **URL Extraction**: Gather new URLs from the HTML content to broaden the crawling frontier.
7. **New URL Cleaning**: Vet new URLs against several filters, such as domain restrictions and visit history.
8. **Queue Updating**: Enqueue permissible URLs for subsequent crawling activities.

Scraping with Local Hash Cache
------------------------------

Users can initialize a scraper with specific domain-related hashes to be stored in memory:

.. code-block:: python

    settings_manager.SCRAPER["HASH_PARTITIONS"] = [
        "fbrefcom",
        "wwweluniversalcommx",
        "abcnewsgocom",
        "wwwcnncom"
    ]

This in-memory storage allows for the rapid identification of previously visited sites, bypassing the need for slower external calls.
Then the Scraper fetch hashes for specified partitions up to a maximum count, thus maintaining a local cache that enhances performance by reducing the number of lookups needed to determine if a URL has already been visited.

