from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    def goToPage(self,url):
        self.driver.get(url)
    
    def getPageSource(self):
        return self.driver.page_source
    
    def getPageSourceCond(self, element):
        delay = 30
        myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
        return self.getPageSource()

    def scrollPageToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def clearLink(self):
        self.urlList = []
    
    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass