import requests
from bs4 import BeautifulSoup
from collections import deque
from pymongo import MongoClient
from selenium import webdriver
import datetime

class ZeldaCrawler(BasicCrawler):
    """Custom ZeldaCrawler class to solve Ocarina of Time speed run challenge.

    Inherits most functionality from BasicCrawler class.

    Uses custom parsing and crawling functions, parse_page_for_profiles and
    crawl respectively.

    Parameters
    ----------

    Attributes
    ----------

    Methods
    -------
    """
    def __init__(self, base_url, db_name, coll_name, use_selenium=False):
        BasicCrawler.__init__(self, base_url, db_name, coll_name, use_selenium)

    def parse_page_for_profiles(self, page_html):
        profiles = []
        soup = BeautifulSoup(page_html, 'html.parser')
        all_anchor_tags = soup.select('a')
        profile_href = 'profiles'
        for anchor_tag in all_anchor_tags:
            try:
                anchor_tag_url = anchor_tag['href']
                if profile_href in anchor_tag_url:
                    profile_url = base_url + anchor_tag_url
                    profile_name = anchor_tag.text
                    profiles.append((profile_url, profile_name))
            except KeyError:
                continue
        return profiles

    def crawl(self, coll_name=None, start_from_base=True,
                    start_page_route=None, start_record_name='start'):
        if coll_name:
            self._connect_to_new_collection(coll_name)
        # scrape and save start page
        self._scrape_and_save_start_page(start_record_name, start_from_base,
                                         start_page_route)
        # parse_start_page_for_links
        start_html = self.load_start_html_from_db()
        profiles = self.parse_page_for_profiles(start_html)
        # use queue to force breadth first search
        profiles_queue = deque(profiles)
        while len(profiles_queue) > 0:
            profile_url, profile_name = profiles_queue.popleft()
            print "Scraping page at {}".format(profile_url)
            print "Scraping profile of user {}".format(profile_name)
            self.scrape_and_save_page(profile_url, profile_name)
