from datalab_api import DatalabShoppingAPI
from pprint import pprint
import json

def main():
    datalab_api = DatalabShoppingAPI()

    category = [{"name":"출산/육아", "param":["50000005"]}, {"name":"식품", "param":["50000006"]}]
    body = datalab_api.CreateBody(startDate="2017-08-01", endDate="2017-08-01", category=category)
    response = datalab_api.CreateRequest(body)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        jobj = json.loads(response_body)
        pprint(jobj)
    else:
        print("Error Code:" + rescode)

if __name__ == "__main__":
    main()