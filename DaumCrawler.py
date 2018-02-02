import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DaumCrawler:
    def __init__(self):
        #os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='
        self.wait = WebDriverWait(self.browser, 1.5)

    def crawl(self, date):
        urls = self.get_targets(date)
        for url in urls:
            self.scroll_to_end(url)
            ###########################

    def scroll_to_end(self, url):
        more_box_xpath = "//div[contains(@class, 'cmt_box')]//div[contains(@class, 'alex_more')]//a[contains(@class,'#more')]"
        page = self.browser.get(url)
        try:
            more_box = self.browser.find_element_by_xpath(more_box_xpath)
            while True:
                more_box.click()
                try:
                    more_box = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, more_box_xpath))
                    )
                except TimeoutException:
                    break
        except:
            pass

    def open_reply(self, comment):
        # cmt_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
        try:
            reply_btn = comment.find_element_by_xpath(".//div[contains(@class, 'box_reply')]//button[contains(@class, '#reply')]//span[contains(@class, 'num_txt')]")
            reply_btn.click()

            more_reply_box_xpath = ".//div[contains(@class, 'reply_wrap')]//div[contains(@class, 'alex_more')]//a[contains(@class,'#more')]"
            more_reply_box = comment.find_element_by_xpath(more_reply_box_xpath)
            while True:
                more_reply_box.click()
                try:
                    more_reply_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, more_reply_box_xpath)))
                except TimeoutException:
                    break
        except NoSuchElementException:
            pass

    def get_targets(self, date):
        query = str(date)
        url = self.base_url + query
        self.browser.get(url)

        li_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_news2')]//li")

        urls = []
        for li in li_list:
            tag_a = li.find_element_by_tag_name('a')
            urls.append(tag_a.get_attribute("href"))
        return urls

if __name__ == '__main__':
    dc = DaumCrawler()
    dc.scroll_to_end('http://v.media.daum.net/v/20180131120719442')
    cmt_list = dc.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
    dc.open_reply(cmt_list[1])