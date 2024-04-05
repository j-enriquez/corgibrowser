Introduction
=============

Web crawling is a critical process in data acquisition from the internet, it has an
important role in indexing and retrieving web content. This section explains the
methodology for ethical and efficient web crawling, adhering to web standards and
respecting site policies.

**Note: Webcrawler module ONLY handles calls to external services, once a call is made, html is retrieved and stored, then Scraper module can Parse the data as many times as needed, this helps reduce complexity of crawling and allow more control**

Crawling Process
----------------------
The web crawling process comprises several key steps:

1 Queue Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Queue Initialization: The crawler begins with retrieving data from multiple
queues, which holds the URLs to be visited from user configuration. Using a queue,
as opposed to local memory, offers several advantages, especially in cloud
computing and big data contexts.
A queue enables distributed processing, allowing multiple crawler instances to work
in parallel. This is essential for handling large-scale web data. It also ensures that
the crawling process can be paused and resumed without loss of state, which is a
limitation with local memory storage. Furthermore, queues facilitate better load
balancing and resource management in cloud environments

2 Buffer Management
~~~~~~~~~~~~~~~~~~~~~~~~~
Buffer Management: A set number of items from the queues are moved
into an in-memory buffer for processing. This buffer acts as a temporary holding
area for URLs, optimizing the data retrieval process.
Buffering allows for batch processing, which reduces the number of I/O operations
and enhances the overall efficiency of the crawler. It also helps in managing
network latency issues, as the crawler processes a batch of URLs rather than
individual requests.

3 Process URL
~~~~~~~~~~~~~~~~~~~
Process the following Steps for each URL on the buffer:

- **a) Domain Extraction:** Extracting the domain from each URL is crucial for steps like fetching robots.txt. It helps in categorizing URLs and applying domain-specific crawling rules.

- **b) Robots.txt Retrieval:** This file, available on most websites, contains directives from website owners on how they prefer their site to be crawled based on allowed or disallowed paths, and throttling. Respecting these rules is essential for ethical crawling. Retrieving and adhering to robots.txt ensures that the crawler does not access or overload parts of the website that the owner intends to keep off-limits for crawlers.

- **c) Review Website Throttling:** Based on Robots.txt or custom website throttling, review if it’s possible to perform the crawling for this URL, if not, continue processing the next item in the queue. If possible to process, update table with new throttling value.

- **d) Sitemap Access:** Accessing sitemap.xml provides a structured overview of a website’s content, allowing for a more organized and comprehensive crawling approach.

- **e) User-Defined Ignoring:** This step allows users to specify certain paths or areas of a site they wish to exclude from crawling, adding an additional layer of customization to the crawling process.

- **f) Compliance Check:** The URL is checked against robots.txt and user-defined ignore paths. This step ensures that the crawler only processes URLs that are allowed and relevant.

- **g) Data Retrieval:** If compliant, the crawler makes an HTTP request to retrieve the HTML document.

- **h) HTML Storage:** The retrieved HTML content is stored in a specified container, bucket, or local folder. This structured storage is essential for efficient data management and retrieval.

Ethical Considerations
----------------------------
Ethical web crawling has a great importance in today’s data environment. Respecting sites specific rules defined in robots.txt, like the URL paths are critical to prevent entering restricted areas. Crawl-delay defined in robots.txt helps to throttle the visits to the site to avoid network damage to owner. This ethical approach ensures that the framework crawling activities consider the principles of digital responsibility where data is retrieved without causing damage to website operations.

Technical Implementation
-------------------------------
The technical implementation of the web crawler considers Python libraries. The crawler programmatically accesses URLs, parses robots.txt and sitemap.xml files, and employs efficient queue and buffer management systems. This setup ensures that the crawler is effective in data retrieval, data management on cloud services, optimized for performance, minimizing resource usage, and maximizing data throughput.

Architectural Overview
----------------------------
The architectural design of the web crawler is to focus on software engineering principles. As part of a larger microservices-based architecture, it operates with other services dedicated to data storage, scraping, and analysis. This modular approach enables scalability and flexibility, allowing the architecture to adapt to varying scales and types of web crawling tasks. Each service is designed to function both independently and as part of a group, ensuring that changes or upgrades can be made with minimal disruption to the overall system.

Practical Application Examples
------------------------------------

- **News Aggregation and Analysis:**
  As example a user selects a group of 5 newspapers for web crawling and scraping. The crawler retrieves articles from these newspapers, storing the HTML content. The scraper then extracts relevant information from these articles. Once the data is collected, data analysis tools are used. This can involve using Language Learning Models (LLMs) like ChatGPT to generate summaries of these articles. Users can perform queries based on specific topics or dates, feeding summaries to another LLM for deeper insights. This can lead to the identification of trends or even the generation of synthesized articles, providing a comprehensive overview of a topic.

- **Academic Research and Model Training:**
  The framework helps academics in collecting and organizing web data. Academics can use the crawler to gather a wide range of web content, which is then stored efficiently in the cloud. This data becomes a valuable resource for training NLP models and LLMs. The accessibility and organization of data in the cloud facilitate collaboration and sharing among researchers, enhancing the scope and scale of academic projects.

- **Business Intelligence and Market Analysis:**
  A  business can use the framework to get market and product information. Custom scrapers can be designed to target specific data, such as pricing or product features, relevant to a business's area. The collected data can be analyzed to identify market trends and consumer preferences. This information can be important in strategic decision-making, such as launching new products or adjusting marketing strategies.
