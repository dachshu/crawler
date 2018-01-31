import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DaumCrawler:
    def __init__(self):
        #os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='

    def scroll_to_end(self, url):
        more_box_xpath = "//div[contains(@class, 'cmt_box')]//div[contains(@class, 'alex_more')]//a[contains(@class,'#more')]"
        page = self.driver.get(url)
        try:
            more_box = self.driver.find_element_by_xpath(more_box_xpath)
            while True:
                more_box.click()
                try:
                    more_box = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, more_box_xpath))
                    )
                except TimeoutException:
                    print('no more box')
        finally:
            return

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

if __name__ == '__main__':
    dc = DaumCrawler()
    dc.scroll_to_end('http://v.media.daum.net/v/20180131120719442')
    cmt_list = dc.driver.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
    print(len(cmt_list))
