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
df= df[df["expiryDate"] == "06-Dec-2023"]
df[df.openInterest > 0]
        
# req_list = ["strikePrice","expiryDate","underlying","lastPrice","instrumentType"]



# df_selected = df[req_list]
# ded = '06-Dec-2023'
# df_filtered = df_selected[df_selected['expiryDate'] == ded]
# # df_new = df_filtered[df_filtered['strikePrice'] == 46900]

# df_filtered