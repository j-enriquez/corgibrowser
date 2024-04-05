Intro
===================================

Overview of the DataManagement Module
-------------------------------------

The DataManagement module is a core component of the CorgiBrowser framework, designed to abstract complex data management operations. It facilitates seamless interaction with cloud storage solutions, focusing on enhancing the efficiency and scalability of web crawling and scraping activities.

Initialization Process
----------------------

The module's initialization process is crucial for setting up the necessary infrastructure for data management, which includes system tables, queues, and containers. Each of these components plays a distinct role in the framework's overall functionality:

Domain Specific Tables/Queue/Container Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialized automatically by the Cloud Provided module:

- Table: **<websitedomain>**: Specific tables for domain-related data management.
- Queue: **<websitedomain>**: Dedicated queues for domain-specific messaging and tasks.
- Container: **<websitedomain>**: For domain-specific HTML content storage.
- Container: **<websitedomain>-JSON-UNKNOWN**: Stores processed HTML content as JSON for domains without custom templates.
- Container: **<websitedomain>-JSON-<CUSTOM VALUE>**: Contains HTML content processed into JSON by custom templates, specific domain requirements.

System Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **corgiwebthrottling**: Ensures domains are accessed at respectful frequencies by managing throttling rates.
- **corgiwebsitemaps**: Facilitates site navigation by storing sitemaps URLs.
- **corgiwebrequestslog**: Captures detailed logs of web requests made, including response statuses.
- **corgiwebscrapelog**: Provides a record of scraping actions for auditing and further analysis.
- **corgiwebqueuepreference**: Manages queue processing preferences like message visibility.
- **corgiwebhashtable**: Tracking previously visited URLs to optimize crawling efforts.

System Queues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **corgiweb**: A shared queue utilized by crawlers for general tasks.

System Containers Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **corgirobotscache**: Stores `robots.txt` files, supporting compliant crawling strategies.

Cloud Provider Interface
------------------------

- Utilizes an interface for cloud provider connectivity, ensuring that each connector to a storage provider encapsulates its logic, allowing for easy switching between storage providers.

Method Overview
---------------

- **initialize**: Prepares the system by creating necessary tables, queues, and containers.
- **add_url_to_queue**: Simplifies adding URLs to the processing queue with minimal user input, handling the creation of related storage resources.
