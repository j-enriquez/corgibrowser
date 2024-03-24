from corgibrowser.corgi_cloud_integration.queues_schemas.corgi_web_queue_version_1 import CorgiWebMessageSchemaVersion1
from corgibrowser.corgi_cloud_integration.tables.corgi_web_entity import CorgiWebEntity


class VisitedUrlProcessor:

    def __init__(self, cloud_integration, crawler_processor, crawler_settings=None):
        self.crawler_settings = crawler_settings

        self.domain = None
        self.metadata = None
        self.html_content = None
        self.new_urls = None
        self.url = None

        self.cloud_integration = cloud_integration
        self.crawler_processor = crawler_processor

        self.initialized = False

    def initialize(self,):

        self.domain = self.crawler_processor.domain
        self.url = self.crawler_processor.url
        self.new_urls = self.get_validated_urls( self.crawler_processor.new_urls )
        self.html_content = self.crawler_processor.url_html  # Placeholder for actual content fetching
        self.metadata = self.crawler_processor.url_metadata  # Placeholder for metadata extraction

        self.initialized = True
        print( "     VisitedUrlProcessor: Initialized" )

    def get_validated_urls(self, new_urls):
        new_validated_urls = [ ]
        for new_url in new_urls:
            new_validated_urls.append( new_url )
        return new_validated_urls

    def start(self):
        if not self.initialized: print( "Not initialized" )

        self.process()

    def process(self):
        if self.crawler_settings[ "PROCESS_VISITED_URL" ]:
            print( "     VisitedUrlProcessor: Starting to process visited url" )
            self.process_visited_url()

    def process_visited_url(self):
        tableRow = self.prepare_corgi_web_table_entity(
            domain = self.domain,
            url = self.url,
            status = "Processed")

        # Upload HTML content to Azure Blob Storage
        self.cloud_integration.upload_to_blob(
            data = self.html_content,
            container_name = tableRow.ContainerName,
            blob_name = tableRow.RowKey,
            metadata = tableRow.to_dict() )
        print( "     VisitedUrlProcessor: Uploaded HTML content to Azure Blob Storage" )

        # Update Status of visited row in table
        print( "     VisitedUrlProcessor: prepare_corgi_web_table_entity completed" )
        self.cloud_integration.upsert_url_info_to_table(
            table_name = self.domain,
            entity = tableRow,
            enable_increase_visited = True,
            del_father_url = True)
        print( "     VisitedUrlProcessor: Update Status of visited row in table" )

    def generate_blob_name_old(self, url):
        """
        Generate a unique blob name based on the URL.
        """
        # Simplified example, consider a more robust approach for real applications
        return url.replace( "http://", "" ).replace( "https://", "" ).replace( "/", "_" )

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

    def get_to_visit_url(self, originalDomain, originalUrl):
        if originalUrl.startswith( "/" ):
            full_url = originalDomain + originalUrl
        else:
            full_url = originalUrl
        full_url = self.ensure_scheme( full_url )
        return full_url

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

