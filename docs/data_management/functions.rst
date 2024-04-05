CloudIntegration Class
======================

class CloudIntegration(settings_manager)[source]
------------------------------------------------

Comprehensive integration with cloud services, handling operations like object storage management, authentication, and queue management.

This class facilitates interactions with Cloud services, ensuring efficient management of cloud resources for web crawling and data storage.

Parameters
----------
**settings_manager** (*SettingsManager*)
    An instance of the SettingsManager class for accessing configuration settings.

Methods
-------

**initialize()**
    Initializes system tables, queues, and containers in cloud storage for the web crawling framework.

    This method performs the following operations:
    
    - Creates system tables
    - Initializes system queues
    - Sets up system containers

**add_url_to_queue(url)**
    Adds a URL to the appropriate queue for crawling.

    Parameters:
    - **url** (*str*): The URL to be added to the queue.

    This method performs operations such as:
    
    - Generating a storage-compatible name for the URL.
    - Creating or fetching the corresponding table, queue, and container for the new URL.
    - Adding the URL to the queue preference table and the dedicated queue.


**Modifying Data Management Settings**
------------------------------------------
Loads the cloud provider account name and key::

    settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
