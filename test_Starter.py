
import requests
from requests_toolbelt import MultipartEncoder

querystr = {"QueryString": {"account": "3001331110","password": "abcd1234","account_type": "8","MF": 201}}

for k,v in querystr.items():
    if isinstance(v, dict):
        print(str(v))
        querystr[k] = str(v)


m = MultipartEncoder(fields=querystr)

url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'
resp = requests.post(url, data=m, headers={'Content-Type' : m.content_type})
print(resp.json())



