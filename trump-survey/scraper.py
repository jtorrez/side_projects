import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

class Scraper(object):
    def __init__(self):
        """Initiliazes an empty Scraper object"""
        self.client = MongoClient()
        self.url = None
        self.raw_html = None

    def scrape_html(self, url):
        """Scrape html from input url

        Parameters
        ----------
        url: str
           The url of the website to scrape

        Returns
        -------
        None
        """
        self.url = url
        r = requests.get(url)
        status_code = r.status_code
        if status_code == 200:
            print "Scrape Successful, status code {}".format(status_code)
            self.raw_html = r.content
        else:
            print "Error, status code {}".format(status_code)

    def save_raw_html(self, db_name, collection_name, entry_name):
        """Save the raw html in a MongoDB

        TODO: Add error handling to not insert a duplicate record
        
        Parameters
        ----------
        db_name: str
        collection_name: str
        entry_name: str

        Returns
        -------
        None
        """
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.insert_one({'name': entry_name,
                                        'html': self.raw_html})
        if result.acknowledged:
            result_str = "Successfully inserted record at id num {}"
            print result_str.format(result.inserted_id)
        else:
            print "Error, couldn't insert record."
