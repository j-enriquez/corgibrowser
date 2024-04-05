CorgiWebThrottling Table
================================

This table stores the request frequencies to websites. This mechanism helps in control the rate limits set by websites, preventing overloading and ensuring respectful crawling practices.

**Note: future improvements considers move this to Redis as in-memory distributed caching**

Class Definition
----------------

The class structure is designed to track and enforce throttling limits for each domain. It includes attributes for the domain name, throttling limit in seconds, and the timestamp of the last access.

.. code-block:: python

    class CorgiWebThrottling:
        def __init__(self, domain, rate=None, last_access_time=None):
            self.PartitionKey = "RateLimit"
            self.RowKey = domain
            self.ThrottlingLimitSeconds = rate
            self.LastAccessTime = last_access_time

        @classmethod
        def from_entity(cls, entity):
            # Construct from database entity
            pass

        def to_dict(self):
            # Convert instance to dictionary
            pass

Throttling Process Overview
---------------------------

Before each request to a website, the CorgiBrowser checks if the domain's rate limit has been exceeded. This process involves:

1. **Checking the Current Rate**: Fetching the current throttling information for the domain from the `corgiwebthrottling` table.
2. **Evaluating Access Permission**: Determining if the time elapsed since the last access is within the allowed rate limit.
3. **Updating Rate Limit and Access Time**: If a request is made, updating the domain's last access time and rate limit in the table.

Usage Scenarios
---------------

- **Update Visit Rate**: To update the throttling rate for a domain.
- **Domain Processing Eligibility**: To check if a domain can be processed based on the current throttling constraints, ensuring respectful adherence to rate limits.
- **Visiting a Domain**: Demonstrates how the framework interacts with the throttling information before proceeding with a domain visit.

This throttling mechanism is important for maintaining efficient and respectful interactions with web servers.
