Introduction
===============

Web scraping is an essential process for extracting data from websites. It complements web crawling by retrieving specific information from the crawled pages.

**Note: Webcrawler module ONLY access that was already downloaded, it can be external data from HTML's or internal data loaded in a container, also this module is responsable for finding new URL's and adding them to the queues**

Scraping Process
----------------------
The web scraping process for this area includes the following steps:

1  Local Hash Cashe is initialized
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Based on customized values, user will decide how many items and from which partitions it would like to retrieve to have stored as local cache to manage visited websites, this is to manage an in-memory a list of visited URLs in the form of a sha256 hash object to identify in-memory which new sites are already visited and avoid external calls.

Example of sha256 hash object in hexadecimal:

00000abea062f3f79e76b7008edfb26ca06adb10cc32cb26f4bea3a97434651a


2 Data Retrieval from Cloud Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The scraper reads HTML content of a web page URL previously stored in a cloud-based Blob (Azure, AWS, or local file system). This approach uses cloud computing benefits for scalability and accessibility. Using cloud storage for data retrieval ensures high availability of data and reduces the use of resources on local systems, facilitating large-scale scraping operations. This also helps to reduce the workload from web crawling and allows to parse the downloaded data from websites as needed without incurring throttling.

3 Template Matching for Data Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The scraper searches for a template that matches a schema. This step is crucial to ensure the extracted data is structured and relevant.

4 Data Extraction from Template
--------------------------------------
Information is extracted from the matched template, involving parsing the HTML content to the desired data. This extraction minimizes unnecessary data processing and ensures the scraper collects only the relevant information.

5 Data Storage in Partitioned Database
------------------------------------------
The scraped data selected for Tables is stored in a partitioned database table, facilitating efficient data management and retrieval. Partitioning allows for handling large datasets and improves query performance, an important step for big data applications.

6 Data Storage in Selected Directory
----------------------------------------
Based on custom templates from the user, all the scraped data selected for Objects will be stored in a container specified by user in a JSON format, this facilitates the storage of original HTML documents along with extracted values that are expected to stay stored in JSON.

7 Metadata Updating for Tracking and Analysis
------------------------------------------------
Metadata in the database is updated to reflect the last visit time to the URL and other relevant metrics. This metadata is crucial for analyzing scraping activities, understanding data changes over time, and planning future scraping strategies.

8 URL Extraction
----------------------------
URLs are extracted from the HTML content and expanding the crawl next items to search.

9 New URL Cleaning
----------------------------
Extracted URLs from HTML and sitemaps are cleaned to filter out disallowed or previously visited links. This step is important for maintaining the quality and relevance. It reviews if scraper allows only new websites from the same domain, then validates if website is already visited by local hash, then if User-Agent can fetch those new domains, if domain is on a custom “Not Allowed Domains list” and lastly if URL path is not allowed by custom list provided by user.

10 Queue Updating
----------------------------
New and allowed URLs are added back to the queue for further crawling.
