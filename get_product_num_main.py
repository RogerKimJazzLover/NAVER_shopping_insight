from get_product_num import Browser
from tabulate import tabulate
from urllib import parse
import pandas as pd
import time

def runCrawl(keyword: str):
    browser = Browser()

    #GETTING THE PAGE HTML
    keyword = parse.quote(keyword) #CONVERTS KOREAN TO URL-CHARACTER
    url = f"https://search.shopping.naver.com/search/all?query={keyword}&cat_id=&frm=NVSHATC"
    browser.goToPage(url)
    cur = browser.getPageSource()

    #GETTING THE PRODUCT NUMBER
    start_index = cur.find('<span class="subFilter_num__S9sle">')
    desired_part = cur[start_index+35:start_index+35+15]
    desired_part = desired_part.split("<")
    product_num = int(desired_part[0].replace(',', ''))
    
    browser.driver.quit()
    time.sleep(3)
    print("FINISH!")

def main():
    runCrawl("숏패딩")

if __name__ == "__main__":
    main()