from tabulate import tabulate
from browser import Browser
from urllib import parse
import pandas as pd
import time

def GetPageSource(browser, keyword: str) -> str:
    #GETTING THE PAGE HTML
    keyword = parse.quote(keyword) #CONVERTS KOREAN TO URL-CHARACTER
    url = f"https://search.shopping.naver.com/search/all?query={keyword}&cat_id=&frm=NVSHATC"
    browser.goToPage(url)
    page_source = browser.getPageSource()
    return page_source

def GetProductNumber(page_source: str) -> int:
    #GETTING THE PRODUCT NUMBER
    start_index = page_source.find('<span class="subFilter_num__S9sle">')
    desired_part = page_source[start_index+35:start_index+35+15]
    desired_part = desired_part.split("<")
    product_num = int(desired_part[0].replace(',', ''))
    return product_num

def main():
    data = pd.read_csv("./data/d_top10_keywords.csv", encoding='euc-kr')
    keywords = list(data["Keywords"])
    search_nums = list(data["Monthly_num_search"])

    new_data = {
        "Prodcut_num":[],
        "Competitive_index":[]
    }

    browser = Browser()
    browser.driver.get("https://www.google.com")
    for i in range(9):
        page_source = GetPageSource(browser, keywords[i])
        product_num = GetProductNumber(page_source)

        new_data["Prodcut_num"].append(product_num)
        new_data["Competitive_index"].append(round(product_num / search_nums[i], 2))
        if i > 1:
            if i%10 == 0:
                time.sleep(30)
        else:
            time.sleep(1)
    
    browser.driver.quit()

    new_data = pd.DataFrame(new_data)
    print(tabulate(new_data, headers='keys', tablefmt='psql'))

    data = pd.concat([data, new_data], axis=1)
    print(tabulate(data, headers='keys', tablefmt='psql'))

    data.to_csv("./data/d_top10_keywords.csv", encoding='euc-kr', index=False)

    return 0

if __name__ == "__main__":
    main()