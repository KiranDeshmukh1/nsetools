import streamlit as st
import testcross 
import pandas as pd

selected_symbol = st.selectbox("#### Index ", options=("NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"))



try:
    df, unique_expiry_dates = testcross.getdata(symbol=selected_symbol)
    unique_expiry_dates_formatted = [date.strftime('%d-%b-%Y') for date in unique_expiry_dates]
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()  # Stop the execution of the app if there's an error

selected_date = st.selectbox('#### Select Date', options=unique_expiry_dates_formatted)

try:
    df_filtered = df[df['expiryDate'] == selected_date]
except Exception as e:
    st.error(f"Error filtering data: {e}")
    df_filtered = pd.DataFrame()  # Set an empty DataFrame to prevent further errors

# Raw Data
hide_df_filtered = st.checkbox("Hide Raw Data", value=False)
if not hide_df_filtered:
    st.dataframe(df_filtered)

# Filtered data for use
selected_columns = ['expiryDate', 'underlying_CE', 'underlyingValue_CE', 'lastPrice_CE', 'strikePrice', 'lastPrice_PE']
df_filtered2 = df_filtered[selected_columns]
df_filtered2 = df_filtered2.round(1)

# Add a new column 'strikePrice2' with values from 'strikePrice'
df_filtered2['strikePrice2'] = df_filtered2['strikePrice']

# Set 'strikePrice2' as the index
df_filtered2.set_index('strikePrice2', inplace=True)

# Strategies
# Straddles
df_filtered2['Straddles_1'] = df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']

# Set Strangle_1 to blank where there is no row above or below
df_filtered2['Strangle_1'] = df_filtered2['lastPrice_CE'].shift(-1) + df_filtered2['lastPrice_PE'].shift(+1)
min_index = df_filtered2.index.min()
max_index = df_filtered2.index.max()

# Set Strangle_1 to blank where there is no row above or below
if min_index < max_index and min_index in df_filtered2.index and (min_index + 1) in df_filtered2.index:
    df_filtered2.loc[min_index:min_index + 1, 'Strangle_1'] = ''
    df_filtered2.loc[max_index - 1:max_index, 'Strangle_1'] = ''


# Create a new column 'Strangle_2' with the formula A4 + C2
df_filtered2['Strangle_2'] = df_filtered2['lastPrice_CE'].shift(-2) + df_filtered2['lastPrice_PE'].shift(2)

# Set Strangle_2 to blank where there is no row above or below
# Set Strangle_2 to blank where there is no row above or below
if min_index < max_index and min_index + 2 <= max_index and min_index in df_filtered2.index and (min_index + 2) in df_filtered2.index:
    df_filtered2.loc[min_index:min_index + 2, 'Strangle_2'] = ''


column_order = ['expiryDate', 'underlying_CE', 'underlyingValue_CE', 'Strangle_1', 'Strangle_2', 'Straddles_1',
                'lastPrice_CE', 'strikePrice', 'lastPrice_PE']
df_filtered2 = df_filtered2[column_order].copy()

# Round all values to one decimal point
st.dataframe(df_filtered2)















# import streamlit as st
# import testcross 
# import pandas as pd
# import time





# selected_symbol = st.selectbox("#### Index ",options=("NIFTY","BANKNIFTY","FINNIFTY","MIDCPNIFTY"))
# df, unique_expiry_dates = testcross.getdata(symbol=selected_symbol)

# unique_expiry_dates_formatted = [date.strftime('%d-%b-%Y') for date in unique_expiry_dates]

# selected_date = st.selectbox('#### Select Date',options= unique_expiry_dates_formatted)

# df_filtered = df[df['expiryDate'] == selected_date]





# #Raw Data
# # Add a checkbox to hide/unhide df_filtered
# hide_df_filtered = st.checkbox("Hide Raw Data", value=False)
# if not hide_df_filtered:
#     st.dataframe(df_filtered)




# #filterdata for use

# selected_columns = ['expiryDate', 'underlying_CE','underlyingValue_CE', 'lastPrice_CE', 'strikePrice', 'lastPrice_PE']
# df_filtered2= df_filtered[selected_columns]
# df_filtered2 = df_filtered2.round(1)

# # Add a new column 'strikePrice2' with values from 'strikePrice'
# df_filtered2['strikePrice2'] = df_filtered2['strikePrice']

# # Set 'strikePrice2' as the index
# df_filtered2.set_index('strikePrice2', inplace=True)

# #Strategies

# #Straddles  -----------------------------------------------------------------
# df_filtered2['Straddles_1'] = df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']


# # column_order = ['expiryDate','underlying_CE','underlyingValue_CE','Straddles_1','lastPrice_CE','strikePrice','lastPrice_PE']
# # df_filtered2 = df_filtered2[column_order].copy()

# #Strangles ------------------------------------------------------------------




# df_filtered2['Strangle_1'] = df_filtered2['lastPrice_CE'].shift(-1) + df_filtered2['lastPrice_PE'].shift(+1)
# # Set Stangle_1 to blank where there is no row above or below
# df_filtered2.loc[df_filtered2.index.min(), 'Strangle_1'] = ''
# df_filtered2.loc[df_filtered2.index.max(), 'Strangle_1'] = ''

# # Create a new column 'Stangle_2' with the formula A4 + C2
# df_filtered2['Strangle_2'] = df_filtered2['lastPrice_CE'].shift(-2) + df_filtered2['lastPrice_PE'].shift(+2)
# # Set Stangle_2 to blank where there is no row above or below
# df_filtered2.loc[df_filtered2.index.min():df_filtered2.index.min() + 1, 'Strangle_2'] = ''
# df_filtered2.loc[df_filtered2.index.max() - 1:df_filtered2.index.max(), 'Strangle_2'] = ''





# column_order = ['expiryDate','underlying_CE','underlyingValue_CE','Strangle_1','Strangle_2','Straddles_1','lastPrice_CE','strikePrice','lastPrice_PE']
# df_filtered2 = df_filtered2[column_order].copy()
# # Round all values to one decimal point



# st.dataframe(df_filtered2)










# # selected_expiry_date = st.selectbox('Select Expiry Date', unique_expiry_dates_formatted)


# # expiry_dates = testcross.getdata(symbol=select_Box)[1]
# # select_Box = st.selectbox("##### Expiry Date",options=(expiry_dates))
# # # index_filtered_df = testcross.getdata(symbol=select_Box)
# # # st.dataframe(testcross.getdata(symbol=select_Box))

# #closest_strike = df_filtered.loc[df_filtered['underlyingValue_CE'].sub(df_filtered['strikePrice']).abs().idxmin()]

# # below_rows = df_filtered[df_filtered['strikePrice'] >= closest_strike['strikePrice']].tail(20)
# # above_rows = df_filtered[df_filtered['strikePrice'] < closest_strike['strikePrice']].head(20)

# # result_df = pd.concat([above_rows, pd.DataFrame([closest_strike]), below_rows])



# # ### -- for future updates ## 

# # ## 1. Bar
