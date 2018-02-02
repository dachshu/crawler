import os
import time
import datetime
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
            data_dict = {}
            data_dict['comment'] = {}
            

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
        except NoSuchElementException:
            pass

    def open_reply(self, comment):
        try:
            reply_btn = comment.find_element_by_xpath(".//div[contains(@class, 'box_reply')]//button[contains(@class, '#reply')]//span[contains(@class, 'num_txt')]")
            reply_btn.click()
        except NoSuchElementException:
            return False

        try:
            more_reply_box_xpath = ".//div[contains(@class, 'reply_wrap')]//div[contains(@class, 'alex_more')]//a[contains(@class,'#more')]"
            more_reply_box = comment.find_element_by_xpath(more_reply_box_xpath)
            while True:
                more_reply_box.click()
                try:
                    more_reply_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, more_reply_box_xpath)))
                except TimeoutException:
                    break
        finally:
            return True

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

    def save_comment(self, comment, is_reply=False):
        data = {}

        if not is_reply:
            data['id'] = int(comment.get_attribute('id').replace('comment',''))
        else:
            data['id'] = int(comment.get_attribute('data-reactid').split('.')[-1][1:])
        data['name'] = comment.find_element_by_css_selector('a.link_nick').text

        cmt_time_txt = comment.find_element_by_css_selector('span.txt_date').text
        if '분' in cmt_time_txt:
            now = datetime.datetime.now()
            now = now - datetime.timedelta(minutes=int(cmt_time_txt.replace('분전', '')))
            cmt_time = time.mktime(now.timetuple())
        elif '시간' in cmt_time_txt:
            now = datetime.datetime.now()
            now = now - datetime.timedelta(hours=int(cmt_time_txt.replace('시간전','')))
            cmt_time = time.mktime(now.timetuple())
        else:
            dt = datetime.datetime.strptime(cmt_time_txt, '%Y.%m.%d. %H:%M')
            cmt_time = time.mktime(dt.timetuple())
        data['time'] = cmt_time
        data['text'] = comment.find_element_by_css_selector('p.desc_txt').text

        if not is_reply:
            data['like'] = int(comment.find_element_by_css_selector('button.btn_recomm span.num_txt').text)
            data['diskile'] = int(comment.find_element_by_css_selector('button.btn_oppose span.num_txt').text)

            if self.open_reply(comment):
                data['reply'] = {}
                reply_list = comment.find_elements_by_css_selector('ul.list_reply li')
                for reply in reply_list:
                    r_data = self.save_comment(reply, is_reply=True)
                    data['reply'][r_data['id']] = r_data

        return data

if __name__ == '__main__':
    dc = DaumCrawler()
    dc.scroll_to_end('http://v.media.daum.net/v/20180131120719442')
    cmt_list = dc.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
    print(dc.save_comment(cmt_list[1]))