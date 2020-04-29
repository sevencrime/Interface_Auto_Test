

import requests
import json

url = "http://localhost:3000/v2/user/register"
data = {
        "phone_number": "75089514626",
        "password" : "Abcd1234", 
        "phone_code" : "86"
}

headers =  {
    "Content-Type" : "application/x-www-form-urlencoded",
    "Authorization" : "Basic dGVzdGFwcDI6YWJjZA==",
    "x-api-key" : "cm9vdDphZG1pbg==",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
}
s = requests.session()
resp = s.post(url, data=json.dumps(data), headers=headers, timeout=10)
print(resp.json())
