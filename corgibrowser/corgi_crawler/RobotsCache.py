import urllib.robotparser
import urllib.request
from urllib.parse import urlparse
import socket

class RobotsCache:
    def __init__(self):
        self.robots_parsers = {}  # Dictionary to store RobotFileParser objects
        self.time_out_sites = {}

    def initialize_parser_if_new_domain(self, url):
        """Returns a RobotFileParser object for the given domain."""
        parsed_url = urlparse( url )
        domain = parsed_url.netloc

        is_new_domain = domain not in self.robots_parsers

        self.get_parser(domain)
        robots_txt = None
        if not self.time_out_sites[domain]:
            robots_txt = self.get_robots_txt_content(url)
        return self.robots_parsers[domain], robots_txt, is_new_domain

    def get_parser(self, domain):
        """Returns a RobotFileParser object for the given domain."""
        if domain not in self.robots_parsers:
            # If the parser for the domain doesn't exist, create and read it
            parser = urllib.robotparser.RobotFileParser()
            parser.set_url(f'http://{domain}/robots.txt')

            try:
                print( "get RobotsTXT" )
                socket.setdefaulttimeout( 5 )  # Set timeout to 5 seconds
                parser.read()
                self.robots_parsers[ domain ] = parser
                self.time_out_sites[ domain ] = False
            except Exception as e:
                print( f"Failed to read robots.txt from {domain}. Assuming no restrictions." )
                self.robots_parsers[ domain ] = None
                self.time_out_sites[ domain ] = True

        return self.robots_parsers[domain]

    def can_fetch(self, user_agent, url):
        """Checks if the given user_agent can fetch the given URL."""

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        parser = self.get_parser(domain)

        if not parser or self.time_out_sites[domain]:
            return False

        return parser.can_fetch(user_agent, url)

    def get_sitemap_urls(self, url):
        """Retrieve sitemap URLs from the robots.txt."""
        parsed_url = urlparse( url )
        domain = parsed_url.netloc
        parser = self.get_parser( domain )

        if parser and not self.time_out_sites[domain]:
            # The sitemaps attribute holds the sitemap URLs

            try:
                return parser.site_maps()
            except Exception as e:
                return [ ]
        return [ ]

    def get_crawl_delay(self, url, user_agent='*'):
        """Retrieve the crawl delay for the specified user agent."""
        parsed_url = urlparse( url )
        domain = parsed_url.netloc
        parser = self.get_parser( domain )
        if parser and not self.time_out_sites[domain]:
            # The crawl_delay method returns the delay in seconds
            try:
                return parser.crawl_delay( user_agent )
            except Exception as e:
                return [ ]
        return None

    def get_robots_txt_content(self, url):
        """Retrieve the content of the robots.txt file for a given URL."""
        parsed_url = urlparse( url )
        domain = parsed_url.netloc
        robots_txt_url = f'http://{domain}/robots.txt'

        try:
            print( "Fetching robots.txt content" )
            socket.setdefaulttimeout( 5 )  # Set timeout to 5 seconds
            with urllib.request.urlopen( robots_txt_url ) as response:
                # Read and decode the content to a string
                content = response.read().decode( 'utf-8' )
            return content
        except Exception as e:
            print( f"Failed to fetch robots.txt from {domain}: {e}" )
            return None