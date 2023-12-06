import streamlit as st
import testcross 
import pandas as pd




selected_symbol = st.selectbox("#### Index ",options=("NIFTY","BANKNIFTY","FINNIFTY","MIDCPNIFTY"))
df, unique_expiry_dates = testcross.getdata(symbol=selected_symbol)

unique_expiry_dates_formatted = [date.strftime('%d-%b-%Y') for date in unique_expiry_dates]

selected_date = st.selectbox('#### Select Date',options= unique_expiry_dates_formatted)

df_filtered = df[df['expiryDate'] == selected_date]

st.dataframe(df_filtered)






# selected_expiry_date = st.selectbox('Select Expiry Date', unique_expiry_dates_formatted)


# expiry_dates = testcross.getdata(symbol=select_Box)[1]
# select_Box = st.selectbox("##### Expiry Date",options=(expiry_dates))
# # index_filtered_df = testcross.getdata(symbol=select_Box)
# # st.dataframe(testcross.getdata(symbol=select_Box))


# ### -- for future updates ## 

# ## 1. Bar
