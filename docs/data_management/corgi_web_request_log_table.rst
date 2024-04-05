CorgiWebRequestLog Table
==========================

This table is part of the compliance feature, enabling the detailed logging of HTTP requests made during the crawling process. This class captures the outcome of each request, including the response status code and any reasons for not visiting a site, such as throttling or restrictions defined in `robots.txt`.

Class Definition
----------------

CorgiWebRequestLog is designed to systematically log every web request, providing insights into the crawling behavior and the responses received from web servers. It uses a combination of the domain name and a timestamp to create unique identifiers for each log entry.

.. code-block:: python

    class CorgiWebRequestLog:
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

Usage and Application
---------------------

- **Detailed Request Logging**: Each instance of CorgiWebRequestLog logs information about web requests, including the target URL, the HTTP status code returned, and the instance ID of the crawler or scraper making the request. This detailed logging facilitates the analysis of crawl efficiency and the identification of potential issues.

- **Handling Non-Visited Sites**: In cases where a site is not visited due to either throttling or restrictions from `robots.txt`, CorgiWebRequestLog will include the specific reason for non-visit. This feature is important for maintaining compliance with web standards and optimizing crawl strategies.

- **Insight into Crawling Activities**: By analyzing the logs generated, users can gain insights into the behavior of their crawling setup, including the success rate of requests and common reasons for request failures.

This logging mechanism plays a pivotal role in the CorgiBrowser framework by ensuring transparency and accountability in web crawling activities, and help in the continuous improvement of crawling strategies.
