Queue Partitioning
======================

Dedicated Queues Per Domain
---------------------------

Each website domain have it's own queue within CorgiBrowser's architecture, mirroring the approach used for table partitioning. This design has several advantages in a distributed crawling service:

- **Focused Crawling Operations**: By assigning each domain a separate queue, crawlers can concentrate on a specific subset of URLs, enhancing the efficiency and effectiveness of the crawling process.
- **Priority Management**: Having dedicated queues allows for the assignment of different priorities to different domains. This prioritization helps in resource allocation and strategic planning of the crawling operations.
- **Scalable Architecture**: The system can easily scale horizontally by adding more crawlers, each configured to work on different domain queues. This scalability ensures that the service can handle an increasing number of domains without a significant increase in resource contention or operational complexity.
- **Parallel Processing**: With dedicated queues, multiple crawlers can operate in parallel, each working on a different set of URLs. This parallelism helps in speeding up the crawling process and ensures that a vast array of web resources can be processed concurrently.

**Purpose**

Designed to encapsulate crucial information about URLs for crawling, the `CorgiWebMessageSchemaVersion1` schema provides a standardized format for queue messages, facilitating the management and processing of web resources.

CorgiWebMessageSchemaVersion1
---------------------------------
**Structure**

- **version**: Marks the schema version.
- **toVisitUrl**: The URL designated for crawling.
- **originalDomain**: The originating domain of the URL.
- **originalUrl**: The complete original URL.
- **partitionKey**: Used for data partitioning.
- **rowKey**: A unique identifier for the record.
- **metadata**: Contains additional data pertinent to the crawl.
- **timestamp**: The creation time of the message.
- **status**: Reflects the current processing status of the URL.

**Usage**

Instantiate the `CorgiWebMessageSchemaVersion1` with necessary details and utilize `.to_json()` and `.from_json()` methods for message serialization and deserialization.

**Application of the Schema**

1. **In Data Management**: For generating JSON messages that are uniformly structured.
2. **By the Crawler**: To deserialize messages and process URLs.
3. **Within the Scraper**: To add new URLs to the queue, ensuring a seamless flow of web resources into the crawling pipeline.
