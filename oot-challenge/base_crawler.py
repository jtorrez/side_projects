"""A Crawler class which crawls links from a given start url.

Goal of this project is to re-create a Scrapy style framework where
the Crawler starts at a given url and continues crawling links until
a specified stopping point.

Implemented Ideas
-----------------
* Crawler can start at base url OR use base url to complete a partial
  url that user specifies as the starting page source.
* Minor error handling for base_url and page_source
* Minor error handling and simple status messages for GET requests
* Minor error handling and simple status messages for MongoDB operations
* Crawler saves each page it scrapes in a MongoDB in case there is an
  error during scraping.
* Crawler parses pages for links to follow

TODO
----
* Build testing framework
* Crawler currently stops after one level of crawling, need to implement
  multi-level crawling with stopping criteria
* Enable multi-threading/asynchronous requests framework
* Crawler can use requests library or Selenium as specified by user
* Robust link parsing for links to crawl and proper error raising
* Robust error handling of input urls and proper error raising
* Robust error handling of MongoDB operations and proper error raising
"""

import requests
from bs4 import BeautifulSoup
from collections import deque
from pymongo import MongoClient
from selenium import webdriver
import datetime


class BasicCrawler(object):
    """A Crawler class which crawls links from a given start url.

    WORK IN PROGRESS, SEE MODULE DOCSTRING FOR IMPLEMENTED AND TODO tasks.

    Parameters
    ----------
    base_url: str
        The base url for the site to be crawled.
    db_name: str
        The name of the database in MongoDB to use.
    coll_name: str
        The name of the collection in db_name in MongoDB to use.
    use_selenium: bool (optional, default=False)
        If True, use Selenium to do the scraping.

    Attributes
    ----------
    base_url: str
        The base url for the site to be crawled.
    use_selenium: bool (optional, default=False)
        If True, use Selenium to do the scraping.
    collection: pymongo Collection object
        The connected collection in MongoDB
    driver: selenium Firefox webdriver object (optional, default=None)
        A Selenium webdriver

    Methods
    -------
    get_page_html(page_url):
        Get and return the html from the page at the given URL.
    scrape_and_save_page(url, record_name)
        Scrape the html from the given URL and save it in a MongoDB.
    get_record_from_db(search_terms_dict)
        Return single page of html from the db according to given search terms.
    load_start_html_from_db()
        Return the html of the start page from the db.
    parse_page_for_links(page_html, css_selector)
        Return a list of tags containing links as selected by the css_selector.
    check_link_urls(links)
        Return true if URL is valid, else False.
    crawl(links_css_selector,
          [coll_name, start_from_base, start_page_route, start_record_name])
        Crawl from starting url, saving html of each page in a MongoDB.
    """

    def __init__(self, base_url, db_name, coll_name, use_selenium=False):
        """Initialize a Crawler object."""
        if base_url[-1] != '/':
            base_url = base_url + '/'
        self.base_url = base_url
        self._client = MongoClient()
        self._db = self._client[db_name]
        self.collection = self._db[coll_name]
        self.use_selenium = use_selenium
        if self.use_selenium:
            self.driver = webdriver.Firefox()

    def get_page_html(self, page_url):
        """Get and return the html from the page at the given URL.

        TODO: Finish selenium functionality

        Parameters
        ----------
        page_url: str

        Returns
        -------
        page_html: str
            The raw html of the given url.
        """
        if self.use_selenium:
            self.driver.get(page_url)
            # TODO: finish selenium functionality
        else:
            r = requests.get(page_url)
            status = r.status_code
            if status != 200:
                print "Error getting page, status code: {}".format(status)
                return None
            else:
                print "Successful request, status code: {}".format(status)
                page_html = r.content
                return page_html

    def _get_start_page_html(self, start_from_base, page_route):
        """Return the html of the page to start crawling on."""
        if not start_from_base and not page_route:
            print "If not starting from the base url, provide page_route"
            return None
        else:
            if start_from_base:
                full_page_url = self.base_url
                page_html = self.get_page_html(full_page_url)
            else:
                if page_route[0] == '/':
                    page_route = page_route[1:]
                full_page_url = self.base_url + page_route
                page_html = self.get_page_html(full_page_url)
            return page_html, full_page_url

    def _connect_to_new_collection(self, collection_name):
        self.collection = self._db[collection_name]

    def _insert_one_record(self, data):
        result = self.collection.insert_one(data)
        if result.acknowledged:
            result_str = "Successfully inserted record at id num {}"
            print result_str.format(result.inserted_id)
        else:
            print "Error, couldn't insert record."

    def _make_record_dict(self, record_name, url, page_html, start_page=False):
        data = {'name': record_name,
                'url': url,
                'html': page_html,
                'start_page': start_page,
                'timestamp': datetime.datetime.now()}
        return data

    def _scrape_and_save_start_page(self, start_record_name, start_from_base,
                                    page_route):
        print "Scraping start page..."
        page_html, url = self._get_start_page_html(start_from_base, page_route)
        data = self._make_record_dict(start_record_name,
                                      url,
                                      page_html,
                                      start_page=True)
        print "Saving start page html..."
        self._insert_one_record(data)

    def scrape_and_save_page(self, url, record_name):
        """Scrape the html from the given URL and save it in a MongoDB."""
        page_html = self.get_page_html(url)
        data = self._make_record_dict(record_name,
                                      url,
                                      page_html)
        print "Saving page html..."
        self._insert_one_record(data)

    def get_record_from_db(self, search_terms_dict):
        """Return record from the db according to given search terms."""
        result_dict = self.collection.find_one(search_terms_dict)
        loading_message = "Loading html from url {}"
        loading_message.format(result_dict['url'])
        return result_dict

    def load_start_html_from_db(self):
        """Return the html of the start page from the db."""
        search_term = {'start_page': True}
        start_dict = self.get_record_from_db(search_term)
        if start_dict is None:
            print "No start page in the collection {}".format(coll_name)
            return start_dict
        else:
            loading_message = "Loading html from start page url {}"
            print loading_message.format(start_dict['url'])
            start_html = start_dict['html']
            return start_html

    def parse_page_for_links(self, page_html, css_selector):
        """Return list of tags containing links selected by css_selector."""
        soup = BeautifulSoup(page_html, 'html.parser')
        links = soup.select(css_selector)
        return links

    def check_link_urls(self, links):
        """Return true if URL is valid, else False."""
        pass

    def crawl(self, links_css_selector, coll_name=None, start_from_base=True,
              start_page_route=None, start_record_name='start'):
        """Crawl from starting url, saving html of each page in a MongoDB."""
        # connect to collection
        if coll_name:
            self._connect_to_new_collection(coll_name)
        # scrape and save start page
        self._scrape_and_save_start_page(start_record_name, start_from_base,
                                         start_page_route)
        # parse_start_page_for_links
        start_html = self.load_start_html_from_db()
        links = self.parse_page_for_links(start_html, links_css_selector)
        # use queue to force breadth first search
        links_queue = deque(links)
        while len(links_queue) > 0:
            link_url = queue.popleft()
            print "Scraping page at {}".format(link)
            # TODO: make default record name
            self.scrape_and_save_page(link_url, record_name)
            # TODO: load link html from db
            # TODO: parse link for more links
            # TODO: add new links to queue
