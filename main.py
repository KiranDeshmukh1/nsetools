import pandas as pd
import requests


bnf_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

nf_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

fnf_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY' 

headers = {
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"


}

session = requests.Session()
data = session.get(bnf_url,headers=headers).json()["records"]["data"]
ocdata = []
new_ocdata = [] 

for i in data:
    for j,k in i.items():
        if j == 'PE' or j =='CE':
        
            info = k
            info["instrumentType"] = j
            ocdata.append(info)
        
        
                
            

df = pd.DataFrame(ocdata)

        
df