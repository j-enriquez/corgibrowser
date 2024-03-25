import time

from corgibrowser.corgi_cloud_integration.queues_schemas.corgi_web_queue_version_1 import CorgiWebMessageSchemaVersion1
from corgibrowser.corgi_cloud_integration.tables.corgi_web_entity import CorgiWebEntity
from corgibrowser.corgi_crawler.RobotsCache import RobotsCache
from corgibrowser.corgi_utils.url_hash import UrlHash
from corgibrowser.corgi_webscraping.default_scrape_template import DefaultScrapeTemplate
import json
from urllib.parse import urlparse


class BatchScraperProcessor:
    def __init__(self, cloud_integration,scraper_settings, container_name, max_blobs_per_batch = 100,scraper_dict={},visited_urls_hash=set(),instance_id=""):
        self.cloud_integration = cloud_integration
        self.scraper_settings = scraper_settings
        self.original_container_name = container_name
        self.container_name = container_name
        self.new_urls = set()
        self.father_url = {}
        self.max_blobs_per_batch = max_blobs_per_batch
        self.blobs_to_visit = []
        initialized = False
        self.robots_cache = RobotsCache()
        self.scraper_dict = scraper_dict
        self.visited_urls_hash = visited_urls_hash
        self.instance_id = instance_id

    def get_left_side(self,string):
        left_side = string.split( '-' )[ 0 ] if '-' in string else string
        return left_side

    def initialize(self,):

        self.blobs_to_visit = self.cloud_integration.list_blobs_in_container_n(self.original_container_name,self.max_blobs_per_batch)

        self.initialized = True

    def start(self,):
        if not self.initialized:
            print( f"BatchScraperProcessor: not initialized" )
            raise

        if not self.blobs_to_visit:
            print( f"BatchScraperProcessor: not blobs_to_visit" )
            return

        for blob in self.blobs_to_visit:
            errors_count = 0
            try:
                # 1.- Retrieve Blob Data
                print("processing blob",blob)
                blob_properties = self.cloud_integration.get_blob_properties( container_name = self.original_container_name,blob_name = blob )
                if not blob_properties: continue
                blob_text = self.cloud_integration.get_blob_text( container_name = self.original_container_name,blob_name = blob )
                if not blob_text: continue

                # 2.- Scrape data
                table_row, blob_row, blob_row_links = self.get_scrape_data( blob_properties, blob_text )

                #3.- Save Blob Data and results
                print("save blob")
                print(json.dumps(table_row, indent=4))
                self.save_blob_results(blob_row, blob_properties)
                self.save_table_results(table_row )
                self.cache_new_links(blob_row_links,blob_properties)

                # 4.- Delete old blob
                if self.get_left_side( self.container_name ) != self.original_container_name:
                    print("delete old blob")
                    self.cloud_integration.delete_blob_from_container( container_name = self.original_container_name, blob_name = blob )

                self.cloud_integration.log_request_scrape( self.container_name, blob, "SCRAPED", self.instance_id )
            except Exception as e:
                print("error",e)
                errors_count += 1
                if errors_count > 50:
                    raise

        print("add new URLs")
        self.process_new_urls(blob_properties)

    def cache_new_links(self,blob_row_links,blob_properties):
        for url in blob_row_links:
            self.new_urls.add( url )
            self.father_url[ url ] = blob_properties[ "metadata" ][ "FullUrl" ]

    def get_scrape_data(self,blob_properties,blob_text):
        scrape = DefaultScrapeTemplate(
            partition_key = blob_properties[ 'metadata' ][ 'PartitionKey' ],
            row_key = blob_properties[ 'metadata' ][ 'RowKey' ],
            container_name = self.get_left_side(blob_properties[ 'container' ]),
            object_name = blob_properties[ 'name' ],
            html_text = blob_text,
            config_file = self.scraper_settings,
            get_default_values = True,
            initial_row_values = blob_properties[ 'metadata' ],
            scraper_dict = self.scraper_dict)
        scrape.initialize()
        scrape.scrape()

        blob_row,links = scrape.get_blob_row()
        table_row = scrape.get_table_row()

        return table_row, blob_row, links

    def save_blob_results(self,blob_row,blob_properties):
        json_data = json.dumps( blob_row, indent = 4 )
        # Convert the JSON string to bytes
        bytes_data = json_data.encode( 'utf-8' )

        self.cloud_integration.upload_to_blob(
            data = bytes_data,
            container_name = self.get_left_side(blob_properties[ 'container' ]),
            blob_name = blob_properties[ 'metadata' ][ 'RowKey' ],
            metadata = blob_properties[ 'metadata' ],
            container_suffix = "-" + "json" + "-" + blob_row["ContainerSuffix"])

    def save_table_results(self,table_row):
        self.cloud_integration.upsert_url_info_to_table(
            table_name = self.get_left_side( self.container_name ),
            entity = table_row,
            enable_increase_visited = True,
            del_father_url = True )

    def process_new_urls(self,blob_properties):
        validated_urls = []
        parsed_url = urlparse( blob_properties[ 'metadata' ][ 'OriginalUrl' ] )
        target_domain = parsed_url.netloc

        for url in self.new_urls:

            # 1. Get URL
            clean_visit_url = self.get_to_visit_url(blob_properties[ 'metadata' ]['OriginalDomain'],url)

            # 2. Validate if it's from the same domain
            if self.scraper_settings["ALLOW_ONLY_NEW_URLS_SAME_SITE"]:
                parsed_url = urlparse( clean_visit_url )
                domain = parsed_url.netloc
                # Check if the URL belongs to the target domain
                if domain != target_domain:
                    continue

            # 3. Validate with local hash
            if UrlHash.encode_url(clean_visit_url) in self.visited_urls_hash:
                continue

            # 4. Validate is User-Agent can fetch
            if not self.robots_cache.can_fetch( "*", clean_visit_url ):
                continue

            # 5. Review if domain is not allowed
            if not self.review_if_domain_is_allowed( domain ):
                continue

            # 6. Review if url path is not allowed
            if not self.review_if_url_path_is_allowed( clean_visit_url ):
                continue

            # 4. Add approved URLs to list
            validated_urls.append( clean_visit_url )

        errors_count = 0
        for new_url in validated_urls:
            # Add Urls to the corgiWeb Table

            try:
                # 1. Get tablewesite row
                tableRow = self.prepare_corgi_web_table_entity(
                    domain = blob_properties[ "metadata" ][ "PartitionKey" ],
                    url = new_url,
                    status = "New",
                    father_url = self.father_url[ new_url ] )
                if tableRow.TableName == "INVALID":
                    continue

                # 2. Upsert record in domain partition
                value_exists = self.cloud_integration.upsert_url_info_to_table(table_name = tableRow.TableName,entity = tableRow )
                if value_exists:
                    continue

                # 3. Send message to queue
                message = self.prepare_queue_message( tableRow.OriginalDomain, tableRow.OriginalUrl,
                                                      tableRow.PartitionKey, tableRow.RowKey )
                self.cloud_integration.upsert_to_queue(
                    queue_name = tableRow.TableName,
                    message = message,
                    visibility_timeout = 30,  # Message becomes visible after 30 seconds
                    time_to_live = 86400 * 7  # Message expires after 7 days
                )

                # 4. Add Url to Hash Table
                self.cloud_integration.add_url_to_hash_table(new_url)

            except Exception as e:
                errors_count += 1
                if errors_count > 10000:
                    raise

    def prepare_corgi_web_table_entity(self, domain, url, status, father_url=""):
        """
        Prepare an entity for Azure Table Storage using the CorgiWebEntity class.
        """

        if status == "New":
            full_url = self.get_to_visit_url( domain, url )
        else:
            full_url = url
        full_url = self.ensure_scheme( full_url )

        corgi_web_entity = CorgiWebEntity( partition_key = domain, row_key = full_url, full_url = full_url,
                                           status = status, father_url = father_url )
        return corgi_web_entity


    def review_if_domain_is_allowed(self, domain):

        disallowed_domains = [
            "www.facebook.com",
            "www.instagram.com",
            "twitter.com",
            "www.tiktok.com",
            "wa.me",
        ]

        if domain.lower() in disallowed_domains:
            return False
        else:
            return True

    def review_if_url_path_is_allowed(self, url):
        disallowed_words = {
            "whatsapp.com",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "tiktok.com",
            "wa.me",
            "javascript:popup",
            "mailto:"
        }

        url_lower = url.lower()  # Lowercase the URL once
        return not any( disallowed in url_lower for disallowed in disallowed_words )


    def get_to_visit_url(self, originalDomain, originalUrl):
        if originalUrl.startswith( "/" ):
            full_url = originalDomain + originalUrl
        else:
            full_url = originalUrl
        full_url = self.ensure_scheme( full_url )
        return full_url


    def ensure_scheme(self, url, default_scheme="https://"):
        """
        Ensure the URL has a scheme; if not, prepend a default scheme.

        :param url: The URL to check.
        :param default_scheme: The default scheme to prepend if the URL lacks one.
        :return: The URL with a scheme.
        """
        if "://" not in url:
            url = f"{default_scheme}{url}"
        return url



    def prepare_queue_message(self, originalDomain, originalUrl, partitionKey, rowKey):
        """
        Prepare a message for Azure Queue Storage with a specific structure.
        """

        toVisitUrl = self.get_to_visit_url( originalDomain, originalUrl )

        # Create an instance of MessageSchema with the URL and metadata
        message_schema = CorgiWebMessageSchemaVersion1( toVisitUrl, originalDomain, originalUrl, partitionKey, rowKey )

        # Convert the message schema to a JSON string
        json_message = message_schema.to_json()

        return json_message
