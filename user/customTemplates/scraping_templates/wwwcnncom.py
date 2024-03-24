from bs4 import BeautifulSoup
from parsel import Selector

from corgibrowser.corgi_webscraping.default_scrape_template import ScrapingTemplate


class wwwcnncom(ScrapingTemplate):
    def initialize(self, ):
        self.soup = BeautifulSoup( self.html_text, "lxml" )

    def extra_data(self, ):
        self.sel = Selector( text = self.html_text )

        # if self.sel.xpath( "//meta[@property='og:type' and @content='article']" ):
        #     self.handle_homepage()
        if self.sel.xpath("//main[@class='article__main']" ):
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

        self.extra_keys["h1"] = self.get_image_urls_by_xpath(self.sel,"//meta[@property='og:title']","/@content")
        self.extra_keys[ "images" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='twitter:image']","/@content")
        self.extra_keys[ "category" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='twitter:image']","/@content")

        self.extra_keys[ "author" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@name='author']","/@content")
        self.extra_keys[ "author_date" ] = self.get_image_urls_by_xpath(self.sel,"//meta[@property='article:published_time']","/@content")

        article_sel = self.sel.xpath( "//div[@class='article__content']" )
        self.extra_keys[ "paragraphs" ] = self.extract_all_text(article_sel,"//p")[: 2000 ]

        self.extra_keys["SourceDataField"] = self.extra_keys[ "h1" ] + " " + self.extra_keys["paragraphs"]
        self.extra_keys["SourceDataField"] = self.extra_keys["SourceDataField"][: 2000 ]
