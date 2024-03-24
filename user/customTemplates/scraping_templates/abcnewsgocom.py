from urllib.parse import unquote

from bs4 import BeautifulSoup
from parsel import Selector

from corgibrowser.corgi_webscraping.default_scrape_template import ScrapingTemplate


class abcnewsgocom(ScrapingTemplate):
    def initialize(self, ):
        self.soup = BeautifulSoup( self.html_text, "lxml" )

    def extra_data(self, ):
        self.sel = Selector( text = self.html_text )

        if self.sel.xpath("//meta[@property='og:type' and @content='article']" ):
            self.handle_article()
        else:
            self.extra_keys[ "ContainerSuffix" ] = "unknown2"
        self.extra_keys[ "html_text" ] = self.html_text


    def handle_homepage(self, ):
        self.extra_keys["ContainerSuffix"] = "homepage"
        self.extra_keys[ "images" ] = ""
        self.extra_keys[ "paragraphs" ] = ""
        self.extra_keys[ "html_text" ] = ""

    def handle_article(self, ):
        self.extra_keys[ "ContainerSuffix" ] = "article"

        content_sel = self.sel.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' FITT_Article_main__body')]")
        self.extra_keys["h1"] = self.get_image_urls_by_xpath(self.sel,"//meta[@property='og:title']","/@content")
        self.extra_keys[ "images" ] = self.get_image_urls_by_xpath(content_sel,"//img","/@src")
        self.extra_keys[ "category" ] = self.extract_segment_in_path( unquote(unquote(self.row_key)),0)

        self.extra_keys[ "author" ] = self.get_image_urls_by_xpath( self.sel, "//meta[@name='author']","/@content" )
        self.extra_keys[ "author_date" ] = self.get_image_urls_by_xpath( self.sel,"//meta[@property='lastPublishedDate']","/@content" )

        self.extra_keys[ "paragraphs" ] = self.extract_all_text(content_sel,"//div[contains(concat(' ', normalize-space(@data-testid), ' '), ' prism-article-body')]")

        self.extra_keys["SourceDataField"] = self.extra_keys[ "h1" ] + " " + self.extra_keys["paragraphs"]
        self.extra_keys[ "SourceDataField" ] = self.extra_keys[ "SourceDataField" ][ : 2000 ]