CorgiWebScrapeLog Table
===========================

This Table logs each scrape made to a document, including the URL, the HTTP status code received in response, and the instance identifier of the scraper. This class ensures that every scraping action is accounted for, providing a clear audit of scraping activities.

Class Definition
----------------

The `CorgiWebScrapeLog` class is designed to capture and store details of web scraping operations. It utilizes the current UTC time to generate a unique `RowKey` for each log entry, ensuring each scrape is distinctly logged.


.. code-block:: python

    class CorgiWebScrapeLog:
        def __init__(self, domain, url, status_code, instance_id):
            utc_now = datetime.datetime.utcnow()
            row_key = utc_now.strftime('%Y%m%dT%H%M%SZ')

            self.PartitionKey = CorgiNameGenerator.get_storage_compatible_name(domain)
            self.RowKey = row_key
            self.Url = url
            self.StatusCode = status_code
            self.InstanceId = instance_id

        def to_dict(self):
            return {
                "PartitionKey": self.PartitionKey,
                "RowKey": self.RowKey,
                "Url": self.Url,
                "StatusCode": self.StatusCode,
                "InstanceId": self.InstanceId
            }


Purpose and Usage
-----------------

**Scrape Logging**: Each instance of `CorgiWebScrapeLog` records essential information from web scraping operations, facilitating detailed monitoring and analysis of scraping activities.

**Audit Trail**: By logging the target URL, response status, and the scraper instance ID, this class provides a comprehensive audit trail that aids in troubleshooting and optimizing scraping strategies.

**Data Analysis**: The structured logging approach allows for easy aggregation and analysis of scraping data, enabling insights into patterns of success and failure, as well as potential compliance or efficiency issues.

