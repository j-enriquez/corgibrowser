# CorgiBrowser: Scalable Web Crawling Framework

CorgiBrowser is an open-source Python framework focused at simplifying the process of web crawling and scraping. Built with scalability, efficiency, and ethical data collection in mind, it is designed for researchers, developers, and analysts who require robust data acquisition capabilities.


## Documentation

readthedocs.org/projects/corgibrowser/

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Depencencies](#dependencies)
- [Getting Started](#getting-started)
- [Demos](#demos)
- [Documentation](#documentation)
- [Background](#background)
- [Contributing to CorgiBrowser](#contributing-to-corgibrowser)
- [License](#license)

## Introduction
CorgiBrowser started from the need for a scalable solution that addresses the challenges of modern web crawling and scraping. With the internet's exponential data growth, existing frameworks often fall short in scalability and customizability. CorgiBrowser, is an all tools included framework that focus on ethical data practices, presents a pioneering approach to distributed crawling and data management.

## Key Features

- **Scalability**: Supports large-scale data collection with a microservices architecture, enabling horizontal scaling on cloud platforms.
- **Distributed Crawling**: Offers configurable crawlers with priority settings for tailored crawling strategies.
- **Use of Custom Scraping Templates**: Facilitates the integration of custom templates for precise data extraction.
- **Ethical Crawling**: Complies with robots.txt standards and employs throttling to minimize the impact on web resources.
- **Cloud Integration**: Works with cloud storage solutions for efficient data management and scalability.

## Depencencies

* Python 3.9+
* Works on Linux, Windows
* Azure Storage Account, [(with future support for local storage)](https://github.com/j-enriquez/corgibrowser/issues/2)


## Getting Started

To install CorgiBrowser, run the following command:

```sh
pip install corgibrowser
```

To initialize a Crawler instance:
```sh
import os
from dotenv import load_dotenv
from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_datasets.DataSetsManager import DataSetsManager
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_crawler.crawler import *

# Load Settings Manager
settings_manager = SettingsManager()
load_dotenv()
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

# Set Up cloud
CloudIntegration(settings_manager = settings_manager)
cloud_integration = CloudIntegration( settings_manager = settings_manager )
cloud_integration.initialize()

# Add Initial URLs
for url in DataSetsManager.load_usa_newspaper_urls():
    cloud_integration.add_url_to_queue(url)

# Crawl
crawler = WebCrawler(cloud_integration = cloud_integration, settings_manager=settings_manager )
crawler.initialize()
crawler.start()
```

To initialize a Scraper instance:
```sh
import os
from dotenv import load_dotenv
from corgibrowser.corgi_cloud_integration.cloud_integration import CloudIntegration
from corgibrowser.corgi_settings.SettingsManager import SettingsManager
from corgibrowser.corgi_webscraping.scraper import Scraper

# Load Settings Manager
settings_manager = SettingsManager()
load_dotenv()
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_NAME"] = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
settings_manager.CLOUD["AZURE_STORAGE_ACCOUNT_KEY"] = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

# Set Up cloud
CloudIntegration(settings_manager = settings_manager)
cloud_integration = CloudIntegration( settings_manager = settings_manager )
cloud_integration.initialize()

# Scrape
scraper = Scraper(cloud_integration = cloud_integration, settings_manager=settings_manager )
scraper.initialize()
scraper.start()
```

## Demos

[Link to demo applications and tutorials.](https://github.com/j-enriquez/corgibrowser/tree/main/user)

## Background

Developed for Jose Enriquez's Master's Thesis in Computer Engineering, CorgiBrowser aims to democratize access to web data through ethical and efficient crawling. CorgiBrowser objective is to represent a significant step in merging web crawling, cloud technologies, and data analysis. This integration enhances scalability, efficiency, and the ability to perform comprehensive data processing, establishing a new benchmark in data collection technologies.

## Contributing to CorgiBrowser

Contributors are welcome! Check out the [Open Issues](https://github.com/j-enriquez/corgibrowser/issues) on GitHub for starting points.

## License
CorgiBrowser is released under the [MIT License](https://github.com/j-enriquez/corgibrowser/blob/main/LICENSE), promoting open and unrestricted use and contribution.





