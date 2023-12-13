from selenium import webdriver

class Browser:
    def __init__(self):
        self.driver = self.SetProxy()
        self.driver.implicitly_wait(3)

    def SetProxy(self):
        '''
        UNSUCCESSFUL!!!!!!!!!!!
        '''
        PROXY = "180.183.157.159:8080"

        options = webdriver.ChromeOptions()
        options.add_argument(f'--proxy-server={PROXY}')
        chrome = webdriver.Chrome(options=options)
        return chrome

    def goToPage(self,url):
        self.driver.get(url)
    
    def getPageSource(self):
        return self.driver.page_source

    def scrollPageToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass