from bs4 import BeautifulSoup
from parsel import Selector

from corgibrowser.corgi_webscraping.default_scrape_template import ScrapingTemplate


class wwweluniversalcommx(ScrapingTemplate):
    def initialize(self, ):
        self.soup = BeautifulSoup( self.html_text, "lxml" )

    def extra_data(self, ):
        self.sel = Selector( text = self.html_text )

        if self.sel.xpath( "//meta[@name='mrf:sections' and @content='homepage']" ):
            self.handle_homepage()
        if self.sel.xpath( "//body[contains(concat(' ', normalize-space(@class), ' '), ' homepage')]" ):
            self.handle_homepage()
        if self.sel.xpath( "//h1[contains(concat(' ', normalize-space(@class), ' '), 'home-custom-title')]" ):
            self.handle_homepage()
        if self.sel.xpath( "//meta[@property='og:type']/@content" ) and self.sel.xpath( "//div[contains(concat(' ', normalize-space(@class), ' '), ' encabezado ')]" ) and self.sel.xpath( "//div[contains(@class, 'sc') and contains(@class, 'pl-3')]//p[@itemprop='description']" ):
            self.handle_article()

    def handle_homepage(self, ):
        self.extra_keys["ContainerSuffix"] = "homepage"
        self.extra_keys[ "images" ] = ""
        self.extra_keys[ "paragraphs" ] = ""
        self.extra_keys[ "html_text" ] = ""

    def handle_article(self, ):
        self.extra_keys[ "ContainerSuffix" ] = "article"

        headers_sel = self.sel.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' encabezado ')]")
        self.extra_keys["h1"] = self.get_text_by_xpath(headers_sel,"//h1[contains(@class, 'title') and contains(@class, 'font-bold')]")
        self.extra_keys[ "images" ] = self.get_image_urls_by_xpath(headers_sel,"//picture[contains(@class, 'story__pic') and contains(@class, 'block') and contains(@class, 'w-full') and contains(@class, 'justify-center') and contains(@class, 'flex')]/img","/@data-src")
        self.extra_keys[ "category" ] = self.get_text_by_xpath( headers_sel,"//a[contains(concat(' ', normalize-space(@class), ' '), 'sc__author--category')]")

        headers_sel = self.sel.xpath( "//div[contains(concat(' ', normalize-space(@class), ' '), ' sc__author ')]" )
        self.extra_keys[ "author" ] = self.extract_all_text( headers_sel,"//div[contains(concat(' ', normalize-space(@class), ' '), 'sc__author-nota')]" )
        self.extra_keys[ "author_date" ] = self.extract_all_text( headers_sel,"//span[contains(concat(' ', normalize-space(@class), ' '), 'sc__author--date')]" )

        self.extra_keys[ "paragraphs" ] = self.get_text_by_xpath(self.sel,"//div[contains(@class, 'sc') and contains(@class, 'pl-3')]//p[@itemprop='description']")
        self.extra_keys[ "html_text" ] = ""

        self.extra_keys["SourceDataField"] = self.extra_keys[ "h1" ] + " " + self.extra_keys["paragraphs"]