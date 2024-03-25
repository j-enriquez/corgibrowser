import time
from collections import defaultdict

from .RobotsCache import RobotsCache
from .crawler_processor import *
from .visited_url_processor import VisitedUrlProcessor
from collections import defaultdict
from itertools import cycle, islice

class WebCrawler:
    def __init__(self, cloud_integration, settings_manager=None):
        self.instance_id = CorgiNameGenerator.initialize_instance_id()
        self.crawler_settings = settings_manager.CRAWLER
        self.buffer = []  # Temporary buffer for URLs to be processed
        self.cloud_integration = cloud_integration
        self.crawler_processor = CrawlerProcessor(cloud_integration, set(),self.instance_id, settings_manager.CRAWLER )
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
        asyncio.run( self._start())

    async def _start(self):

        if not self.initialized:
            print("WebCrawler: ERROR - Not Initialized")
            raise

        for x in range(0, self.crawler_settings["CRAWLER_CYCLES_COUNT"]):

            # get items to buffer
            if not self.buffer:
                print( "WebCrawler: Sleep" )
                time.sleep( self.crawler_settings[ "CRAWLER_SLEEP_IN_SECONDS" ] )
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
                    await self.crawler_processor.start()
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
        all_messages = [ ]
        queue_preferences = self.cloud_integration.get_entities_from_table( "corgiwebqueuepreference" )

        for row in queue_preferences:

            # Skip queues not in QUEUE_ONLY_DOMAINS if that setting is enabled
            if self.crawler_settings[ "QUEUE_ONLY_DOMAINS" ] and row[ "RowKey" ] not in self.crawler_settings[
                "QUEUE_ONLY_DOMAINS" ]:
                continue

            # Continue only if there are items to pop
            if row[ "ItemsToPopFromQueue" ] <= 0:
                continue

            # Retrieve messages based on the specified items count and visibility timeout
            queue_name = row[ "RowKey" ]
            items_to_pop = row[ "ItemsToPopFromQueue" ]
            visibility_timeout = row[ "VisibilityTimeout" ]

            # Fetch messages from the queue
            messages = self.cloud_integration.get_messages_from_queue( queue_name, items_to_pop, visibility_timeout )

            # Append messages to the buffer if any
            if messages:
                for msg in messages:
                    msg[ "QueueName" ] = queue_name
                    all_messages.append( msg )

        # Distribute messages in round-robin order to prevent consecutive items from the same queue
        distributed_messages = self.distribute_round_robin( all_messages )

        # Append distributed messages to the buffer
        self.buffer.extend( distributed_messages )

    @staticmethod
    def distribute_round_robin(items):
        # Group items by type (QueueName in this case)
        groups = defaultdict( list )
        for item in items:
            groups[ item[ "QueueName" ] ].append( item )

        # Create a round-robin iterator over the groups
        round_robin_order = cycle( groups.keys() )

        # Limit the cycle to the total number of items to prevent infinite loop
        limited_round_robin = islice( round_robin_order, len( items ) )

        distributed = [ ]
        for key in limited_round_robin:
            if groups[ key ]:  # If there are still items left in this group
                distributed.append( groups[ key ].pop( 0 ) )

        return distributed