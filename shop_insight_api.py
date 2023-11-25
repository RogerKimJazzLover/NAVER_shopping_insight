import os
import sys
import json
import urllib.request
from pprint import pprint

client_id = ""
client_secret = ""
url = "https://openapi.naver.com/v1/datalab/shopping/categories"

startDate = "2017-08-01"
endDate = "2017-09-30"

body = {
    "startDate":startDate,
    "endDate":endDate,
    "timeUnit":"month",
    "category":[{"name":"출산/육아", "param":["50000005"]}, {"name":"식품", "param":["50000006"]}],
    "device":"pc",
    "ages":["20","30"],
    "gender":"f"
}
body = json.dumps(body)

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    jobj = json.loads(response_body)
    pprint(jobj)
else:
    print("Error Code:" + rescode)