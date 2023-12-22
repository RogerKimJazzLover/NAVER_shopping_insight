from datalab_api import DatalabSearchAPI
import reusable_funcs
import custom_exceptions
from pprint import pprint
from tqdm import tqdm
import pandas as pd
import json

def GetResponse(datalab_api, keywords: list) -> json:
    keywords_groups = datalab_api.CreateKeywordsGroups(keywords)
    body = datalab_api.CreateBody(startDate="2023-11-20", endDate="2023-12-20", keywords_groups=keywords_groups)
    response = datalab_api.GetResponse(body)
    rescode = response.getcode()

    if rescode != 200:
        raise custom_exceptions.ResponseError(rescode)
    
    response_body = response.read()
    jobj = json.loads(response_body)
    print(type(jobj))
    return jobj

def main():
    #1. Initializing values
    datalab_api = DatalabSearchAPI()
    table = pd.read_csv(f"./data/m_top10_keywords.csv", encoding="euc-kr")
    keywords = list(table["Keywords"])

    #2.. Getting the endDate(yesterday) and startDate(1 month ago)
    endDate = reusable_funcs.GetEndDate()
    startDate = reusable_funcs.GetStartDate(endDate, 'm')
    endDate = endDate.strftime('%Y-%m-%d')
    startDate = startDate.strftime('%Y-%m-%d')

    for i in tqdm(range(5, 6001, 5)):
        temp_keywords = keywords[i-5:i]
        pprint(GetResponse(datalab_api, temp_keywords))


if __name__ == "__main__":
    main()