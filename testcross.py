import pandas as pd
import requests
from datetime import datetime

def getdata(symbol):
    url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'
    


    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        data = response.json()["records"]["data"]
        exp_dates = response.json()["records"]["expiryDates"]
        
        
        ocdata = []
        
        
        for i in data:
            for j, k in i.items():
                if j == 'PE' or j == 'CE':
                    info = k
                    info["instrumentType"] = j
                    ocdata.append(info)

        
            

            
        
            
        df = pd.DataFrame(ocdata)
        df_pe = df[df['instrumentType'] == 'PE']
        df_ce = df[df['instrumentType'] == 'CE']
        merged_df = pd.merge(df_ce, df_pe, on=['strikePrice', 'expiryDate'], suffixes=('_CE', '_PE'), how='outer')

        
        
        df_exp_dates = pd.DataFrame({'Date': exp_dates})
        unique_expiry_dates = df_exp_dates['Date'].unique()
        unique_expiry_dates = sorted(pd.to_datetime(unique_expiry_dates, format='%d-%b-%Y'))

        return merged_df,unique_expiry_dates

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None


    
