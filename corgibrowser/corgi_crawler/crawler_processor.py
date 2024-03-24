import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from corgibrowser.corgi_cloud_integration.queues_schemas.corgi_web_queue_version_1 import CorgiWebMessageSchemaVersion1
from corgibrowser.corgi_utils.names_generator import CorgiNameGenerator


class CrawlerProcessor:
    def __init__(self, cloud_integration, visited_urls, crawler_settings=None):
        self.crawler_settings = crawler_settings
        self.cloud_integration = cloud_integration

        self.visited_urls = visited_urls  # Keep track of visited URLs to avoid re-crawling
        self.domain = ""
        self.url = ""
        self.url_html = ""
        self.url_metadata = ""
        self.new_urls = []
        self.robots_parser = None
        self.constraint = ""

        self.initialized = False

    def initialize(self, json_message,domain,robotsCache):
        self.constraint = None
        self.robotsCache = robotsCache
        self.json_message = json_message
        self.domain = domain

        self.initialized = True

        print("     CrawlerProcessor: Initialized")

    def start(self,):

        if not self.initialized:
            print("     CrawlerProcessor: ERROR - Not Initialized" )

        self.process_url(self.json_message.toVisitUrl)

        print("     CrawlerProcessor: Completed")

    def process_url(self, url):
        self.url = url
        """Process a single URL."""
        print(f"     CrawlerProcessor: Processing Url{self.url}")

        if not self.is_allowed_by_robots(self.url) or self.is_throttled(self.domain) or not self.is_allowed_by_user(self.url):
            print("     CrawlerProcessor: Request was not processed due to constraint")
            return False  # Indicate that URL was not processed due to constraints
        else:
            print( "     CrawlerProcessor: URL not have constraints")

        # Retrieve and process HTML content
        self.retrieve_html(url)


        self.get_metadata()
        if self.url_html:
            new_urls = self.extract_urls(self.url_html)
            print(f"     CrawlerProcessor: found urls {len(new_urls)}" )
            self.new_urls = new_urls  # Return new URLs extracted from the content for the caller to manage
            return True
        print( "     CrawlerProcessor: failure to process urls" )
        return False  # Indicate failure to process URL

    def is_allowed_by_robots(self, url):
        """Check if crawling is allowed by robots.txt.
            b) Robots.txt Retrieval: This file, available on most websites, contains directives
            from website owners on how they prefer their site to be crawled based on allowed or
            disallowed paths, and throttling. Respecting these rules is essential for ethical
            crawling.
            Retrieving and adhering to robots.txt ensures that the corgi_crawler does not access or
            overload parts of the website that the owner intends to keep off-limits for crawlers.
        """
        user_agent = "*"
        if self.robotsCache.can_fetch( user_agent, url ):
            print( f"{user_agent} can access {url}" )
            return True
        else:
            print( f"{user_agent} cannot access {url}" )
            self.constraint = "NotAllowed"
            return False


    def is_throttled(self, domain):
        """Check if the URL is throttled.
            c) Review Website Throttling: Based on Robots.txt or custom website throttling,
            review if it’s possible to perform the crawling for this URL, if not, continue
            processing the next item in the queue. If possible, to process, update table with new
            throttling value.
        """
        can_process = self.cloud_integration.can_process_domain(domain)

        print(f"     CrawlerProcessor: allowed based on domain throttle {can_process}")
        # Placeholder for throttling check

        if not can_process:
            self.constraint = "Throttled"

        return not can_process

    def is_allowed_by_user(self, url):
        """Check if crawling is allowed by user.
            e) User-Defined Ignoring: This step allows users to specify certain paths or areas
            of a site they wish to exclude from crawling, adding an additional layer of
            customization to the crawling process.
        """
        if not self.review_if_url_path_is_allowed( url ):
            self.constraint = "NotAllowed"
            return False
        print( f"     CrawlerProcessor: allowed based on user logic {True}" )
        # Placeholder for user checking logic
        return True

    def retrieve_html(self, url):
        """Retrieve HTML content and process it.
            g) Data Retrieval: If compliant, the corgi_crawler makes an HTTP request to retrieve the
            HTML document.
        """
        self.cloud_integration.visit_domain(self.domain)

        try:
            response = requests.get(url, timeout=5)

            self.cloud_integration.log_request( self.domain, url, response.status_code )
            if response.status_code == 200:
                self.url_html = response.text
                print( "     CrawlerProcessor: HTML retrieved" )
            else:
                print( response )
                print( response.__dict__ )
                self.constraint = "NoHTML"
                print( "     CrawlerProcessor: HTML not retrieved" )

        except Exception as e:
            self.cloud_integration.log_request(self.domain,url, "Timeout" )


    def get_metadata(self):
        print(f"     CrawlerProcessor: Metadata Retrieved {True}")

    def extract_urls(self, html_content):
        """Extract URLs from HTML content.
            i) URL Extraction: URLs are extracted from the HTML content and the sitemap,
            expanding the crawl next items to search.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a', href=True)
        return [link['href'] for link in links]

    def review_if_url_path_is_allowed(self, url):

        disallowed_words = [
            "whatsapp://send",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "tiktok.com",
            "wa.me",
            "javascript:popup"
        ]

        for disallowed in disallowed_words:
            if disallowed.lower() in url.lower():
                return False

        return True
