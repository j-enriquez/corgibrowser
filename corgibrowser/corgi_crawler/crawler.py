import time
from .RobotsCache import RobotsCache
from .crawler_processor import *
from .visited_url_processor import VisitedUrlProcessor

class WebCrawler:
    def __init__(self, cloud_integration, settings_manager=None):
        self.crawler_settings = settings_manager.CRAWLER
        self.buffer = []  # Temporary buffer for URLs to be processed
        self.cloud_integration = cloud_integration
        self.crawler_processor = CrawlerProcessor(cloud_integration, set(),settings_manager.CRAWLER )
        self.visited_urls_processor = VisitedUrlProcessor(cloud_integration, self.crawler_processor,settings_manager.CRAWLER)
        self.robotsCache = RobotsCache()
        self.initialized = False
        self.urls_visited = None

    def initialize(self):

        if self.crawler_settings["ENABLE_CORGIWEB_QUEUE"]:
            self.cloud_integration.add_domain_to_queue_preference_table("corgiweb", self.crawler_settings["CORGIWEB_QUEUE_ITEMS_TO_POP"], 18000)

        self.urls_visited = 0
        self.manage_buffer()

        self.initialized = True
        print("WebCrawler: Initialized")

    def start(self):

        if not self.initialized:
            print("WebCrawler: ERROR - Not Initialized")
            raise

        for x in range(0, self.crawler_settings["CRAWLER_CYCLES_COUNT"]):

            # get items to buffer
            if not self.buffer:
                self.manage_buffer()
                print( "WebCrawler: Get more items from queue" )

            # Process items from buffer
            errors_count = 0
            while self.buffer:

                if self.urls_visited >= self.crawler_settings["CRAWLER_URLS_TO_VISIT"]:
                    return
                else:
                    self.urls_visited +=1

                # get message to process
                message = self.buffer.pop( 0 )

                try:
                    # 1. Read message to JSON
                    json_message = CorgiWebMessageSchemaVersion1.from_json( message.content )
                    toVisitUrl = json_message.toVisitUrl
                    domain = CorgiNameGenerator.extract_domain(toVisitUrl)
                    print( "WebCrawler: Read message to JSON",domain, toVisitUrl )

                    # 2. Process Robots Txt
                    self.manage_robots_cache( domain, toVisitUrl )
                    print( "WebCrawler: Processed Robots Txt" )

                    # 3. Visit Url and extract it's data
                    self.crawler_processor.initialize(json_message,domain, self.robotsCache)
                    self.crawler_processor.start()
                    print( "WebCrawler: Visited Url and extract it's data")

                    # 4. Handle Contraints
                    if self.crawler_processor.constraint in ["NotAllowed","NoHTML","Throttled"]:
                        if self.crawler_processor.constraint in ["NotAllowed","NoHTML"]:
                            self.cloud_integration.delete_message_from_queue( message[ "QueueName" ], message )
                        continue
                    print( "WebCrawler: Handled Contraints" )

                    # 5. Manage Visited Url
                    self.visited_urls_processor.initialize()
                    self.visited_urls_processor.start()
                    print( "WebCrawler: Manage Visited Url")

                    # 6. Delete message from queue
                    self.cloud_integration.delete_message_from_queue( message[ "QueueName" ], message )
                except Exception as e:
                    self.cloud_integration.delete_message_from_queue( message[ "QueueName" ], message )
                    errors_count +=1
                    if errors_count > 100:
                        raise

            time.sleep(self.crawler_settings["CRAWLER_SLEEP_IN_SECONDS"])

    def manage_robots_cache(self,domain,toVisitUrl):
        robots_parsers, robots_txt, is_new_domain = self.robotsCache.initialize_parser_if_new_domain(toVisitUrl)

        if is_new_domain and robots_parsers:

            sitemaps = self.robotsCache.get_sitemap_urls( toVisitUrl )
            if sitemaps:
                self.cloud_integration.save_sitemaps( domain, sitemaps )

            crawl_delay = self.robotsCache.get_crawl_delay( toVisitUrl )
            if crawl_delay:
                self.cloud_integration.update_visit_rate( domain, crawl_delay )

            if robots_txt:
                self.cloud_integration.save_robots_txt_blobs( robots_txt, domain )


    def manage_buffer(self,):

        for row in self.cloud_integration.get_entities_from_table("corgiwebqueuepreference"):

            if self.crawler_settings["QUEUE_ONLY_DOMAINS"]:
                if row["RowKey"] not in self.crawler_settings["QUEUE_ONLY_DOMAINS"]:
                        continue

            if row["ItemsToPopFromQueue"] > 0:

                messages = self.cloud_integration.get_messages_from_queue( row["RowKey"], row["ItemsToPopFromQueue"], row["VisibilityTimeout"] )

                if messages:
                    for msg in messages:
                        msg[ "QueueName" ] = row["RowKey"]
                        self.buffer.append( msg )
