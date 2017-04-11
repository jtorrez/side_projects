import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import *
from stem import Signal
from stem.control import Controller
from faker import Faker
import random
import os

class SurveyBot(object):
    """TODO: Actually finish this"""
    def __init__(self, survey_url, auto_nav=True):
        self.driver = webdriver.Firefox()
        self.url = survey_url
        self.fake = Faker()
        if auto_nav:
            self.open_page()

    def open_page(self):
        self.driver.get(self.url)

    def click_buttons(self):
        pass

    def click_checkboxes(self):
        pass

    def fill_one_text_box(self, box_id, filler_text):
        textbox = self.driver.find_element_by_id(box_id)
        textbox.send_keys(filler_text)

    def fill_text_boxes(self, text_box_ids, filler_text_list):
        pass

    def fill_contact_info(self):
        pass


class TrumpSurveyBot(object):
    def __init__(self, survey_url, yes_questions,
                 no_questions, auto_nav=True, anon=False):
        self.ProxyHost = "127.0.0.1"
        self.ProxyPort = "8118"
        if anon:
            self.driver = self._change_proxy()
        else:
            self.driver = webdriver.Firefox()
        self.url = survey_url
        self.fake = Faker()
        if auto_nav:
            self.open_page()
        self.yes_questions = yes_questions
        self.no_questions = no_questions
        self.issue_checkbox = 'question_3386'
        self.issues = ['Conservatism']
        self.network_checkbox = 'question_3387'
        self.networks = ['CNN', 'MSNBC', 'Local news']
        self.my_source_box_id = 'id_question_3388'
        self.my_sources = ['New York Times',
                           'Washington Post',
                           'LA Times']
        self.online_sources_id = 'id_question_3390'
        self.my_online_sources = ['The Atlantic',
                               'Huffington Post',
                               'National Review']
        self.name_id = 'id_full_name'
        self.email_id = 'id_email'
        self.zip_id = 'id_postal_code'

    def _change_proxy(self):
        "Define Firefox Profile with you ProxyHost and ProxyPort"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", self.ProxyHost )
        profile.set_preference("network.proxy.http_port", int(self.ProxyPort))
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.ssl", self.ProxyHost )
        profile.set_preference("network.proxy.ssl_port", int(self.ProxyPort))
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.ftp", self.ProxyHost )
        profile.set_preference("network.proxy.ftp_port", int(self.ProxyPort))
        profile.update_preferences()
        return webdriver.Firefox(firefox_profile=profile)

    def _set_new_ip(self):
        """Change IP using TOR"""
        passphrase = os.environ['TOR_PASS']
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=passphrase)
            controller.signal(Signal.NEWNYM)

    def open_page(self):
        self.driver.get(self.url)

    def click_buttons(self, button_names, button_value):
        for name in button_names:
            css_selector_str = "input[type='radio'][name='{0}'][value='{1}']"
            css_format_str = css_selector_str.format(name, button_value)
            button = self.driver.find_element_by_css_selector(css_format_str)
            button.click()

    def click_checkboxes(self, box_name, box_values):
        for value in box_values:
            css_str = "input[type='checkbox'][name='{0}'][value='{1}']"
            css_format_str = css_str.format(box_name, value)
            checkbox = self.driver.find_element_by_css_selector(css_format_str)
            checkbox.click()

    def fill_one_text_box(self, box_id, filler_text):
        textbox = self.driver.find_element_by_id(box_id)
        textbox.send_keys(filler_text)

    def fill_fake_contact_info(self, name_id, email_id, zip_id):
        fake_name = self.fake.name()
        fake_email = self.fake.email()
        fake_zipcode = self.fake.zipcode()
        self.fill_one_text_box(name_id, fake_name)
        self.fill_one_text_box(email_id, fake_email)
        self.fill_one_text_box(zip_id, fake_zipcode)

    def submit_form(self):
        css_str = "input[type='submit'][name='respond']"
        submit_button = self.driver.find_element_by_css_selector(css_str)
        submit_button.click()

    def clean_up(self):
        self.driver.quit()

    def display_current_ip(self):
        self.driver.get("https://www.iplocation.net/find-ip-address")
        time.sleep(10)

    def using_tor(self):
        self.driver.get("http://check.torproject.org/")
        exp_text = 'Congratulations. This browser is configured to use Tor.'
        act_text = self.driver.find_element_by_css_selector("h1.not").text
        return exp_text == act_text

    def take_one_survey(self):
        self.click_buttons(self.yes_questions, 'Yes')
        self.click_buttons(self.no_questions, 'No')
        self.click_checkboxes(self.issue_checkbox, self.issues)
        self.click_checkboxes(self.network_checkbox, self.networks)
        random_my_source = random.choice(self.my_sources)
        random_online_source = random.choice(self.my_online_sources)
        self.fill_one_text_box(self.my_source_box_id, random_my_source)
        self.fill_one_text_box(self.online_sources_id, random_online_source)
        self.fill_fake_contact_info(self.name_id, self.email_id, self.zip_id)
        time.sleep(3)
        self.submit_form()

    def repeat_survey(self, repeat_num):
        self._set_new_ip()
        for num in xrange(repeat_num):
            self.open_page()
            self.take_one_survey()
            self._set_new_ip()
            time.sleep(2)
            if not self.using_tor():
                print "No longer private! Terminating loop."
                break
            else:
                print """I'm still using Tor, continuing.
                         I've take the survey {} times
                         \n""".format(num)
            if num % 5 == 0:
                self.display_current_ip()
