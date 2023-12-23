from datalab_api import DatalabSearchAPI
import reusable_funcs
import custom_exceptions

import json, time, os
from tqdm import tqdm
import pandas as pd
import numpy as np

@reusable_funcs.ReAttemptUntilFailure(max_attempt=3, time=10)
def GetResponse(datalab_api, keywords: list, startDate: str, endDate: str) -> dict:
    keywords_groups = datalab_api.CreateKeywordsGroups(keywords)
    body = datalab_api.CreateBody(startDate=startDate, endDate=endDate, keywords_groups=keywords_groups)
    response = datalab_api.GetResponse(body)
    rescode = response.getcode()

    if rescode != 200:
        raise custom_exceptions.ResponseError(rescode)
    
    response_body = response.read()
    jobj = json.loads(response_body)
    return jobj

def CreateDateColumns(response, table):
    desired_part = response["results"][0]["data"]
    for i in range(len(desired_part)):
        table[desired_part[i]["period"]] = []

def AppendRatio(response, table):
    dates = response["results"][0]["data"]
    for i in range(5):
        #For each keywords
        for day in range(len(dates)):
            #For each day of each keyword
            try:
                ratio = response["results"][i]["data"][day]["ratio"]
                table[dates[day]["period"]].append(ratio)
            except IndexError:
                print("!ERROR: INDEX ERROR, APPENDING NaN")
                table[dates[day]["period"]].append(np.nan)

def main():
    #1. Initializing values
    datalab_api = DatalabSearchAPI()

    file_name = os.environ.get('FILE_NAME', './data/test.csv')
    table = pd.read_csv(file_name, encoding="euc-kr")
    keywords = list(table["Keywords"])

    #2. Getting the endDate(yesterday) and startDate(1 month ago)
    endDate = reusable_funcs.GetEndDate()
    startDate = reusable_funcs.GetStartDate(endDate, 'm')
    endDate = endDate.strftime('%Y-%m-%d')
    startDate = startDate.strftime('%Y-%m-%d')

    #3. Initializing new data
    new_data = {}
    '''
    going to look something like...
    {
        "2023-11-20" : [24,42,12,1,23,.......] (len = 60000)
        "2023-11-21" : [24,42,12,1,23,.......] (len = 60000)
        .
        .
        (len = 30)
    }
    '''

    #4. Completing the new data table
    for i in tqdm(range(5, len(keywords)+1, 5)):
        temp_keywords = keywords[i-5:i]
        response = GetResponse(datalab_api, temp_keywords, startDate, endDate)
        if i == 5:
            #INITIALIZING THE COLUMNS AS THE DATES IN THE FIRST LOOP
            CreateDateColumns(response, table=new_data)
        AppendRatio(response, new_data)
    print(new_data['2023-11-25'])
    print(len(new_data['2023-11-25']))

    #5. Appending the new data to the old table
    for key, value in new_data.items():
        table[str(key)] = value

    save_as = os.environ.get('SAVE_AS', './data/test.csv')
    table.to_csv(save_as, encoding="euc-kr", index=False)

if __name__ == "__main__":
    main()