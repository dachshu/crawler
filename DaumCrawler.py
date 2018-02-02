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

    def crawl(self, date):
        urls = self.get_targets(date)
        
        for url in urls:
            self.browser.get(url)

            news = self.parse_news(url)

            self.scroll_to_end(url)
            #댓글 파싱 

            #write
            


    def parse_news(self, url):
        news_id = url.split('/')[-1]
        news_title = self.browser.find_element_by_xpath("//h3[contains(@class, 'tit_view')]").text
        news_open_time = None
        news_modi_time = None
        news_reporter = None
        for txt_info in self.browser.find_elements_by_xpath("//span[contains(@class, 'info_view')]//span[contains(@class, 'txt_info')]"):
            info = txt_info.text
            if info[0] == '입' and info[1] == '력': news_open_time = info[2:]
            elif info[0] == '수' and info[1] == '정': news_modi_time = info[2:]
            else : news_reporter = info
        news_press = self.browser.find_element_by_xpath("//div[contains(@class, 'head_view')]//img").get_attribute('alt')
        news_body = self.browser.find_element_by_xpath("//div[contains(@class, 'article_view')]").text
        news = {'id' : news_id, 'title' : news_title, 'time' : news_open_time, 'modi_time' : news_modi_time, 'writer' : news_press, 'reporter' : news_reporter, 'text' : news_body }
        return news

    def scroll_to_end(self, url):
        more_box_xpath = "//div[contains(@class, 'cmt_box')]//div[contains(@class, 'alex_more')]//a[contains(@class,'#more')]"
        page = self.browser.get(url)
        waiting_time = 2
        try:
            more_box = self.browser.find_element_by_xpath(more_box_xpath)
            while True:
                more_box.click()
                try:
                    more_box = WebDriverWait(self.browser, waiting_time).until(
                        EC.element_to_be_clickable((By.XPATH, more_box_xpath))
                    )
                except TimeoutException:
                    print('no more box')
                    cmt_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
                    print(len(cmt_list))
        finally:
            return

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
    dc.crawl(20180131)