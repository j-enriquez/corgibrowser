from bs4 import BeautifulSoup

from corgibrowser.corgi_webscraping.default_scrape_template import ScrapingTemplate


class fbrefcom(ScrapingTemplate):
    def initialize(self, ):
        self.soup = BeautifulSoup( self.html_text, "lxml" )
    def extra_data(self, ):
        self.extra_keys["html_text"] = self.html_text
