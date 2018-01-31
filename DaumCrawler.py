import os
import time
from selenium import webdriver


class DaumCrawler:
    def __init__(self):
        #os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='

    def get_targets(self, date):
        query = str(date)
        url = self.base_url + query
        self.browser.get(url)
        time.sleep(1)

        li_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_news2')]//li")

        urls = []
        for li in li_list:
            tag_a = li.find_element_by_tag_name('a')
            urls.append(tag_a.get_attribute("href"))
        return urls
