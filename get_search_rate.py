from datalab_api import DatalabSearchAPI
from pprint import pprint
import json

def main():
    datalab_api = DatalabSearchAPI()

    keywords_groups = datalab_api.CreateKeywordsGroups(group_name="숏패딩", keywords=["숏패딩"])
    body = datalab_api.CreateBody(startDate="2023-11-20", endDate="2023-12-20", keywords_groups=keywords_groups)
    response = datalab_api.GetResponse(body)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        jobj = json.loads(response_body)
        pprint(jobj)
    else:
        print("Error Code:" + rescode)

if __name__ == "__main__":
    main()