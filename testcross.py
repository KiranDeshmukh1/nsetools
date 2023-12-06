import pandas as pd
import requests


def getdata(symbol = 'BANKNIFTY'):
    url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'

    # nf_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

    # fnf_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY' 

    headers = {
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"


    }

    session = requests.Session()
    data = session.get(url,headers=headers).json()["records"]["data"]
    ocdata = []
    

    for i in data:
        for j,k in i.items():
            if j == 'PE' or j =='CE':
            
                info = k
                info["instrumentType"] = j
                ocdata.append(info)
            
            
                    
                

    df = pd.DataFrame(ocdata)
    df_pe = df[df['instrumentType'] == 'PE']
    df_ce = df[df['instrumentType'] == 'CE']
    
    # Assuming df_ce and df_pe are the DataFrames you obtained
    merged_df = pd.merge(df_ce, df_pe, on=['strikePrice', 'expiryDate'], suffixes=('_CE', '_PE'), how='outer')

    
    
    
    
    unique_expiry_dates = merged_df['expiryDate'].unique()
    unique_expiry_dates = sorted(pd.to_datetime(unique_expiry_dates, format='%d-%b-%Y'))
    


    return merged_df ,unique_expiry_dates
    
getdata(symbol="NIFTY")
    
    
    
    
    # # Find the index of the row with strikePrice closest to underlyingValue
    # closest_index = (df_merged['strikePrice'] - df_merged['underlyingValue_x']).abs().idxmin()

    # # Extract the surrounding 20 rows above and below the closest_index
    # start_index = max(0, closest_index - 20)
    # end_index = min(df_merged.shape[0] - 1, closest_index + 20)

    # selected_rows = df_merged.iloc[start_index:end_index + 1]

    # return selected_rows
            
    
