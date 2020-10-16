import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['https://firststop.sos.nd.gov/search/business']
    start_urls = ['https://firststop.sos.nd.gov/search/business/']

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        
    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_class_name("search-input").send_keys("X")
        #searchButton = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/main/div/div/button')
        #searchButton.click()
        self.driver.find_element_by_class_name("advanced-search-toggle").click()
        activeOnly = self.driver.find_element_by_xpath("//*[@id='field-ACTIVE_ONLY_YN']")
        activeOnly.click()
        searchButton = self.driver.find_element_by_class_name("btn btn-primary btn-raised advanced-search-button")
        table = self.driver.find_element_by_class_name("div-table center-container")
        pass


