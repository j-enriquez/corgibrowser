import time
from .batch_scraper_processor import *
from ..corgi_utils.names_generator import CorgiNameGenerator


class Scraper:
    def __init__(self, cloud_integration, settings_manager=None, scraper_dict = {} ):
        self.instance_id = CorgiNameGenerator.initialize_instance_id()
        self.scrapper_settings = settings_manager.SCRAPER
        self.cloud_integration = cloud_integration
        self.containers_to_visit = None
        self.robotsCache = RobotsCache()
        self.initialized = False
        self.scraper_dict = scraper_dict
        self.visited_urls_hash = set()

    def initialize(self):
        self.get_containers_to_visit()

        if self.scrapper_settings["HASH_PARTITIONS"]:
            self.visited_urls_hash = self.cloud_integration.retrieve_hash_for_partitions( self.scrapper_settings["HASH_PARTITIONS"], self.scrapper_settings["HASH_MAX_COUNT"] )

        self.initialized = True
        print( "WebScrapper: Initialized" )

    def start(self):

        if not self.initialized:
            print( "WebScrapper: ERROR - Not Initialized" )

        for x in range( 0, self.scrapper_settings[ "SCRAPER_CYCLES_COUNT" ] ):

            for container in self.containers_to_visit:
                print( f"WebScrapper: visiting {container}" )
                try:
                    batchProcessor = BatchScraperProcessor( self.cloud_integration,
                                                            self.scrapper_settings,
                                                            container,
                                                            max_blobs_per_batch = self.scrapper_settings["MAX_BLOBS_PER_BATCH"],
                                                            scraper_dict=self.scraper_dict,
                                                            visited_urls_hash = self.visited_urls_hash,
                                                            instance_id = self.instance_id)
                    batchProcessor.initialize()

                except Exception as e:
                    print( container, "not found" )
                    continue

                batchProcessor.start()

            print( "time to sleep" )
            time.sleep( self.scrapper_settings[ "SCRAPE_SLEEP_IN_SECONDS" ] )

    def get_containers_to_visit(self, ):

        containers_to_visit = [ ]

        if self.scrapper_settings[ "ONLY_DOMAINS" ]:
            for only_container in self.scrapper_settings[ "ONLY_DOMAINS" ]:
                containers_to_visit.append( only_container )
        else:
            for row in self.cloud_integration.get_entities_from_table( "corgiwebqueuepreference" ):
                containers_to_visit.append( row[ "RowKey" ] )
        self.containers_to_visit = list( set( containers_to_visit ) )
