import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from urllib.parse import unquote_plus
import requests
import json
from parsel import Selector

class DefaultScrapeTemplate:
    def __init__(self, partition_key, row_key, container_name, object_name, html_text, config_file, get_default_values=True, initial_row_values=None,scraper_dict={}):
        self.row = {}
        if initial_row_values:
            for k,v in initial_row_values.items():
                self.row[k]=v

        self.config = config_file
        self.get_default_values = get_default_values

        self.html_text = html_text
        self.process_html_text()


        self.object_name = object_name
        self.container_name = container_name
        self.partition_key = partition_key
        self.row_key = row_key

        # Initialize instance variables
        self.default_h1 = ""
        self.metadata = {}
        self.links = []
        self.images = ""
        self.paragraphs = ""

        # Initialize limits
        self.h1_limit = self.config['H1_LIMIT']
        self.max_images = self.config[ 'MAX_IMAGES' ]
        self.max_paragraph_length = self.config[ 'MAX_PARAGRAPH_LENGTH' ]
        self.max_links = self.config[ 'MAX_LINKS' ]

        self.scraper_dict = scraper_dict

        self.initialized = False

    def process_html_text(self,):
        try:
            # Attempt to load the string as JSON
            parsed_json = json.loads( self.html_text )

            # Check if 'html_text' key exists in the JSON object
            if 'html_text' in parsed_json:
                self.html_text = parsed_json[ 'html_text' ]
                print( "Updated html_text from JSON." )
            else:
                print( "JSON does not contain 'html_text' key." )
        except json.JSONDecodeError:
            # If self.html_text is not JSON, do nothing
            print( "html_text is not a valid JSON string." )

    def initialize(self):
        if self.container_name in self.scraper_dict.keys():
            scrapertemplate = self.scraper_dict[ self.container_name ]( self.html_text,self.row_key )
            self.html_text = scrapertemplate.html_text
            self.soup = scrapertemplate.soup
        else:
            scrapertemplate = default(self.html_text,self.row_key)
            self.html_text = scrapertemplate.html_text
            self.soup = scrapertemplate.soup
            print("not there")
        print(self.container_name ,self.scraper_dict.keys())
        self.initialized = True

    def scrape(self):

        if not self.initialized:
            raise Exception("Scraper : Not Initialized")

        if self.get_default_values:
            self.row["get_default_values"] = self.get_default_values
            self.row["h1"] = self.extract_h1()
            self.row["metadata"] = self.extract_metadata()
            self.row["links"] = self.extract_links()
            # self.row["images"] = self.extract_images()
            self.row["paragraphs"] = self.extract_paragraphs()
            self.row[ "html_text" ] = self.html_text
            self.row[ "Status" ] = "Scraped"
            self.row["ContainerSuffix"] = "unknown"
        self.find_extra_data()

    def get_blob_row(self,):
        links = self.row["links"]
        # if "links" in self.row:
        #     del self.row[ "links" ]
        return self.row,links

    def get_table_row(self,):
        self.row[ "Status" ] = "Scraped"
        tmp_row = self.row.copy()

        for k in ["links","images","html_text","paragraphs","metadata"]:
            if k in tmp_row.keys():
                del tmp_row[k]

        filtered_dict = {}
        for key, value in tmp_row.items():
            # Check if the value is neither a list nor a dictionary
            if not isinstance( value, (list, dict) ):
                filtered_dict[ key ] = value

        return filtered_dict

    def extract_h1(self):
        # Extract h1 text up to specified limit
        h1 = ""
        for heading in self.soup.find_all(["h1"]):
            if len(h1) + len(heading.text.strip()) <= self.h1_limit:
                h1 += heading.text.strip() + " "
            else:
                break
        return h1

    def extract_metadata(self):
        # Extract common metadata into a dictionary
        metadata = {}
        for meta in self.soup.find_all("meta"):
            name = meta.get("name", meta.get("property", "")).lower()
            if name:
                metadata[name] = meta.get("content", "")
        return metadata

    def extract_links(self):
        # Initialize an empty list to store the links
        links = [ ]

        # Iterate over all <a> tags with an href attribute
        for link in self.soup.find_all( "a", href = True ):
            # Check if we've reached the maximum number of links to extract
            if self.max_links is not None and len( links ) >= self.max_links:
                break  # Exit the loop if the maximum limit is reached

            # Extract the href attribute (link URL)
            href = link.get( "href" )
            if href:
                links.append( href )  # Add the link to the list

        return links

    def extract_images(self):
        # Extract source URLs for images up to the specified maximum
        return "images"

    def extract_paragraphs(self):
        # Concatenate text from all paragraph tags up to the specified maximum length
        paragraphs = ""
        for p in self.soup.find_all("p"):
            new_paragraph_text = p.text.strip()
            if self.max_paragraph_length is None or len(paragraphs) + len(new_paragraph_text) <= self.max_paragraph_length:
                paragraphs += new_paragraph_text + " "
            else:
                break
        return paragraphs

    def find_extra_data(self):
        if self.container_name in self.scraper_dict.keys():
            extra_keys = self.scraper_dict[self.container_name](self.html_text,self.row_key).extra_keys
            self.row.update(extra_keys)

class ScrapingTemplate:
    def __init__(self, html_text, row_key):
        self.extra_keys = {}
        self.html_text = html_text
        self.row_key = row_key
        self.soup = BeautifulSoup( self.html_text, "lxml" )
        self.extra_data()
    def initialize(self):
        # Base method to be overridden by derived classes
        pass
    def extra_data(self):
        # Base method to be overridden by derived classes
        pass

    def get_image_urls_by_xpath(self, selector: Selector, xpath: str, type):
        """
        Receives an XPath expression and a Selector object, and returns the URLs of images selected by the XPath as a list.

        :param selector: The Selector object to apply the XPath on.
        :param xpath: The XPath expression to select <img> elements or directly their @src attributes.
        :return: A list of strings, each representing the URL of an image.
        """
        # If the XPath targets <img> elements, append '/@src' to select the src attribute.
        # If the XPath already targets @src, this modification is not needed.
        # For flexibility, this method assumes the XPath could be either way.
        if not xpath.endswith( type ):
            xpath_modified = xpath + type
        else:
            xpath_modified = xpath

        # Using .xpath() on the Selector to select the attribute based on the modified XPath
        # .get() is used to return the first match or None if there are no matches
        first_image_url = selector.xpath( xpath_modified ).get()

        return first_image_url

    def get_text_by_xpath(self, selector: Selector, xpath: str):
        """
        Receives an XPath expression and a Selector object, and returns the text inside the selected elements as a list.

        :param selector: The Selector object to apply the XPath on.
        :param xpath: The XPath expression to select elements with.
        :return: A list of strings, each representing the text of a selected element.
        """
        # Modifying the XPath to select the text nodes of the elements
        # This is done by appending '/text()' to the provided XPath expression
        xpath_modified = xpath + "/text()"

        # Using .xpath() on the Selector to select text nodes based on the modified XPath
        selected_text_nodes = selector.xpath( xpath_modified )

        # Extracting text from each selected text node and joining them into a single string
        # Spaces or another delimiter can be used to separate text from different nodes, if desired
        concatenated_text = ''.join( element.get() for element in selected_text_nodes )

        return concatenated_text

    def extract_all_text(self,selector: Selector, xpath: str) -> str:
        """
        Extracts all text nodes within the given XPath and returns them as a single string.

        :param selector: The Selector object to apply the XPath on.
        :param xpath: The XPath expression to select elements with.
        :return: A single string containing all text nodes concatenated together.
        """
        # Selecting all text nodes within the given XPath
        text_nodes = selector.xpath( f'{xpath}//text()' ).getall()

        # Concatenating all text nodes into a single string, separating by spaces
        # This also removes any leading/trailing whitespace from each text node
        all_text = ' '.join( text.strip() for text in text_nodes if text.strip() )

        return all_text

    def extract_segment_in_path(self, url, segment_index):
        # Parsing the URL to extract components
        parsed_url = urlparse( url )

        # Extracting the path, splitting by "/", and filtering out any empty strings
        # (which occur due to leading "/")
        path_segments = [ segment for segment in parsed_url.path.split( "/" ) if segment ]
        print("extract_segment_in_path",url,path_segments)
        # Retrieving the specified path segment, if available
        segment_to_return = path_segments[ segment_index ] if len( path_segments ) > segment_index else ""

        return segment_to_return

class default(ScrapingTemplate):
    #suggested extra fields
    "ContainerSuffix"
    "images"
    "paragraphs"
    "html_text"
    "h1"
    "images"
    "category"
    "author"
    "author_date"
    "paragraphs"
    "html_text"
    "SourceDataField"

    def initialize(self, ):
        self.soup = BeautifulSoup( self.html_text, "lxml" )
    def extra_data(self, ):
        self.extra_keys["html_text"] = self.html_text

#
# scraper_dict = {
#     "fbrefcom": fbrefcom,
#     "wwweluniversalcommx": wwweluniversalcommx,
#     "abcnewsgocom": abcnewsgocom,
#     "wwwcnncom": wwwcnncom
# }
#
#
# if __name__ == "__main__":
#     # El universal test
#     # url = "https://www.eluniversal.com.mx/elecciones/luis-donaldo-colosio-riojas-recibe-licencia-para-contender-por-el-senado/"
#     # url = "https://www.eluniversal.com.mx/"
#     # response = requests.get(url, timeout=5)
#     # if response.status_code == 200:
#     #     html_text = response.text
#     #     print( "     CrawlerProcessor: HTML retrieved" )
#     # else:
#     #     print( "     CrawlerProcessor: HTML not retrieved" )
#     # with open( '../corgi_settings/scraper_settings.json', 'r' ) as config_file:
#     #     scraper_settings = json.load(config_file)
#     # scrape = DefaultScrapeTemplate(
#     #     partition_key="wwweluniversalcommx",
#     #     row_key="",
#     #     container_name="wwweluniversalcommx",
#     #     object_name="",
#     #     html_text=html_text,
#     #     config_file=scraper_settings,
#     #     get_default_values=True,
#     #     initial_row_values=None)
#     # scrape.initialize()
#     # scrape.scrape()
#     # blob_row = scrape.get_blob_row()
#     # del blob_row["links"]
#     # # del blob_row[ "images" ]
#     # del blob_row[ "html_text" ]
#     # print("save blob")
#     # print(json.dumps(blob_row, indent=4))
#
#     #abcnews
#     # url = "https://abcnews.go.com/Lifestyle/redefines-means-run-girl/story?id=24377039"
#     # # url = "https://www.eluniversal.com.mx/"
#     # response = requests.get( url, timeout = 5 )
#     # if response.status_code == 200:
#     #     html_text = response.text
#     #     print( "     CrawlerProcessor: HTML retrieved" )
#     # else:
#     #     print( "     CrawlerProcessor: HTML not retrieved" )
#     # with open( '../corgi_settings/scraper_settings.json', 'r' ) as config_file:
#     #     scraper_settings = json.load( config_file )
#     # scrape = DefaultScrapeTemplate(
#     #     partition_key = "abcnewsgocom",
#     #     row_key = "http%253A%252F%252Fabcnews.go.com%252F2020%252Fschizophrenia-children-families-grapple-costs-emotional-financial%252Fstory%253Fid%253D10053795",
#     #     container_name = "abcnewsgocom",
#     #     object_name = "",
#     #     html_text = html_text,
#     #     config_file = scraper_settings,
#     #     get_default_values = True,
#     #     initial_row_values = None )
#     # scrape.initialize()
#     # scrape.scrape()
#     # blob_row,links = scrape.get_blob_row()
#
#     # cnncom
#     url = "https://www.cnn.com/2012/03/30/us/trayvon-martin-profile/index.html"
#     response = requests.get( url, timeout = 5 )
#     if response.status_code == 200:
#         html_text = response.text
#         print( "     CrawlerProcessor: HTML retrieved" )
#     else:
#         print( "     CrawlerProcessor: HTML not retrieved" )
#     with open( '../corgi_settings/scraper_settings.json', 'r' ) as config_file:
#         scraper_settings = json.load( config_file )
#     scrape = DefaultScrapeTemplate(
#         partition_key = "wwwcnncom",
#         row_key = "http%253A%252F%252Fabcnews.go.com%252F2020%252Fschizophrenia-children-families-grapple-costs-emotional-financial%252Fstory%253Fid%253D10053795",
#         container_name = "wwwcnncom",
#         object_name = "",
#         html_text = html_text,
#         config_file = scraper_settings,
#         get_default_values = True,
#         initial_row_values = None )
#     scrape.initialize()
#     scrape.scrape()
#     blob_row, links = scrape.get_blob_row()
#     # del blob_row[ "html_text" ]
#     print( "save blob" )
#     print( json.dumps( blob_row, indent = 4 ) )
#
