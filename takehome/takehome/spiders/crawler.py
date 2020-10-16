import scrapy
from selenium import webdriver

class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['https://firststop.sos.nd.gov/search/business']
    start_urls = ['https://firststop.sos.nd.gov/search/business/']

    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def parse(self, response):
        self.driver.get(response.url)
        searchInput = self.driver.find_element_by_class_name("search-input")
        searchInput.send_keys("X")
        advSearch = self.driver.find_element_by_class_name("advanced-search-toggle")
        advSearch.click()
        activeOnly = self.driver.find_element_by_xpath("//*[@id='field-ACTIVE_ONLY_YN']")
        activeOnly.click()
        searchButton = self.driver.find_element_by_class_name("btn btn-primary btn-raised advanced-search-button")
        searchButton.click()
        pass


