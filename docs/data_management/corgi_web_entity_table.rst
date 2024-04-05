Table Partitioning
=========================================================

CorgiWebEntity
---------------------------

Designed to represent and store individual web entities. This allows for horizontal scalable storage of data by partitioning the entities across multiple tables based on the domain of the URL, with each domain stored in its own dedicated table.

**Note: For Azure tables due to it's partitions is in consideration to move everything to a single table, leaving multiple tables for initial stages until direction is defined as there might be partitioning by StorageAccount as well**

Table Partitioning Overview
---------------------------

Managing the partitions is handled by the Framework private methods on CloudIntegration, `upsert_url_info_to_table` is responsible for managing the partitioned tables. It performs several key operations:

1. **Initialization**: If table not exists, creates new table
2. **Visited Count Management**: Increases the visited count if the entity exists, or initializes it if the entity is new.
3. **Upsert Operation**: Updates the entity's information in the table.

By partitioning the tables per domain, the system can scale horizontally, as new tables are created to accommodate entries for each new domain. This approach enhances performance by segmenting data and improving query response times.

CorgiBrowser simplifies the data management process by automating table partitioning. As part of its crawling operations, when the system encounters different domains, it systematically creates and stores each domain's data in a separate table. Users do not need to handle any aspect of the partitioning themselves. It allows for a clean separation of data and efficient management, enhancing performance for large-scale crawling operations.

Example of Partitioned Tables
-----------------------------

Here are some illustrative examples of how CorgiBrowser might partition the data into tables based on domain names:

Crawler_Queue -> (abc, domain1, domain2, domain3)

On processing each of the domains it will call it's internal method `upsert_url_info_to_table` and determine where to store the data

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Domain
     - Table URL
   * - abc
     - `https://mystorageaccount.table.core.windows.net/abc`
   * - domain1
     - `https://mystorageaccount.table.core.windows.net/domain1`
   * - domain2
     - `https://mystorageaccount.table.core.windows.net/domain2`
   * - domain3
     - `https://mystorageaccount.table.core.windows.net/domain3`

These tables are generated dynamically to accommodate the data associated with each unique domain encountered during web crawling.


CorgiWebEntity Schema
---------------------

Each `CorgiWebEntity` instance corresponds to a unique URL and contains all the necessary attributes to represent and manage it within the system:

- **PartitionKey**: A name generated from the URL to serve as the partition key.
- **RowKey**: A unique identifier for the entity within the partition.
- **ContainerName** and **BlobName**: Designators for blob storage, corresponding to the entity.
- **TableName**: The name of the table in which the entity is stored.
- **OriginalDomain** and **OriginalUrl**: The domain and the full URL of the entity.
- **FullUrl**: The complete URL of the entity.
- **FatherUrl**: The URL of the parent page from which this entity was derived, if applicable.
- **Status**: The current status of the entity, such as 'visited' for crawled URLs or 'new' for freshly discovered URLs.

Usage in Web Crawling and Scraping
-----------------------------------

When a crawler visits a URL, the `CorgiWebEntity`'s status is updated to reflect this. Similarly, when the scraper discovers new URLs, they are added to the appropriate table, and custom templates provided by the user can dictate additional data storage behaviors. This structured approach ensures that each entity is appropriately categorized and accessible for ongoing and future processing tasks.
