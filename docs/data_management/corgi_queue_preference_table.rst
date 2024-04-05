CorgiWebQueuePreference Table
==========================================

Table designed to manage the behavior of message retrieval from queues.

Class Definition
----------------

The class provides a structure for storing preferences related to queue processing, such as the number of items to process at a time and the visibility timeout for each item. These settings are crucial for effective load balancing and resource management during crawling operations.

.. code-block:: python

    class CorgiWebQueuePreference:
        def __init__(self, partition_key, row_key, items_to_pop_from_queue, visibility_timeout):
            self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(partition_key)
            self.RowKey = CorgiNameGenerator.get_storage_compatible_name(row_key)
            self.ItemsToPopFromQueue = items_to_pop_from_queue
            self.VisibilityTimeout = visibility_timeout

        def to_dict(self):
            return {
                "PartitionKey": self.PartitionKey,
                "RowKey": self.RowKey,
                "ItemsToPopFromQueue": self.ItemsToPopFromQueue,
                "VisibilityTimeout": self.VisibilityTimeout
            }

Usage in Queue Management
-------------------------

Data from the CorgiWebQueuePreference table is utilized to dictate how the WebCrawler or Scraper instances manage and retrieve messages from the queues. The configuration specifies the quantity of messages to fetch and how long they should remain invisible to other consumers once popped.

High-Level Overview
-------------------

- **ItemsToPopFromQueue**: Determines the number of messages to retrieve from the queue at one time.
- **VisibilityTimeout**: Defines the duration for which a message is invisible in the queue after being popped.

Example Configuration
---------------------

A practical example of setting up a crawler with targeted domains can be achieved by configuring `QUEUE_ONLY_DOMAINS` within the `settings_manager`:

.. code-block:: python

    # Setup targeted domains for crawling
    settings_manager.CRAWLER["QUEUE_ONLY_DOMAINS"] = [
        "fbrefcom",
        "wwweluniversalcommx",
        "abcnewsgocom",
        "wwwcnncom"
    ]

In this configuration, the crawler will specifically target queues that correspond to the defined domains, optimizing the crawling process for these selected sites. This approach can lead to a more focused crawl and potentially reduce resource consumption and processing time.
