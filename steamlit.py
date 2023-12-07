import streamlit as st
import testcross
import pandas as pd

# Initialize session state
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = "NIFTY"
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

# Function to update df_filtered2 based on current selection
def update_data():
    try:
        df, unique_expiry_dates = testcross.getdata(symbol=st.session_state.selected_symbol)
        unique_expiry_dates_formatted = [date.strftime('%d-%b-%Y') for date in unique_expiry_dates]
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()  # Stop the execution of the app if there's an error

    try:
        df_filtered = df[df['expiryDate'] == st.session_state.selected_date]
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        df_filtered = pd.DataFrame()  # Set an empty DataFrame to prevent further errors

    # Filtered data for use
    selected_columns = ['expiryDate', 'underlying_CE', 'underlyingValue_CE', 'lastPrice_CE', 'strikePrice', 'lastPrice_PE']
    df_filtered2 = df_filtered[selected_columns]
    df_filtered2 = df_filtered2.round(1)

    # Add a new column 'strikePrice2' with values from 'strikePrice'
    df_filtered2['strikePrice2'] = df_filtered2['strikePrice']

    # Set 'strikePrice2' as the index
    df_filtered2.set_index('strikePrice2', inplace=True)

    # Strategies###############################################################
    
    # Straddles ---------------------------------------------------------------
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
    if min_index < max_index and min_index + 2 <= max_index and min_index in df_filtered2.index and (
            min_index + 2) in df_filtered2.index:
        df_filtered2.loc[min_index:min_index + 2, 'Strangle_2'] = ''
        
        
    
    
    #SPREADS
    #CALL SPREADS ----------------------------------------------------------
    
    #Call Spread 1 -------
    
    df_filtered2['Spread_1_C'] = df_filtered2['lastPrice_CE'] - df_filtered2['lastPrice_CE'].shift(-1)
    
    #Call Spread 2 -------
    
    df_filtered2['Spread_2_C'] = df_filtered2['lastPrice_CE'] - df_filtered2['lastPrice_CE'].shift(-2)
    
    #Call Spread 3 -------
    
    df_filtered2['Spread_3_C'] = df_filtered2['lastPrice_CE'] - df_filtered2['lastPrice_CE'].shift(-3)
    
        
    #PUT SPREADS --------------------------------------------------------------
    
    #Put Spread 1 -----
    
    df_filtered2['Spread_1_P'] = df_filtered2['lastPrice_PE'] - df_filtered2['lastPrice_PE'].shift(+1)
    
    #Put Spread 2 -------
    
    df_filtered2['Spread_2_P'] = df_filtered2['lastPrice_PE'] - df_filtered2['lastPrice_PE'].shift(+2)
    
    #Put Spread 3 -------
    
    df_filtered2['Spread_3_P'] = df_filtered2['lastPrice_PE'] - df_filtered2['lastPrice_PE'].shift(+3)
    
    
    
    
    
    
    #BUTTERFLY
    #CALL BUTTERFLY ----------------------------------------------------------
    
    #Call butterfly 1 -------
    
    df_filtered2['btrfly_1'] = (df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']) - (df_filtered2['lastPrice_CE'].shift(-1) + df_filtered2['lastPrice_PE'].shift(+1))
    
    #Call butterfly 2 -------
    
    df_filtered2['btrfly_2'] = (df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']) - (df_filtered2['lastPrice_CE'].shift(-2) + df_filtered2['lastPrice_PE'].shift(+2))
    
   #Call butterfly 3 -------
    
    df_filtered2['btrfly_3'] = (df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']) - (df_filtered2['lastPrice_CE'].shift(-3) + df_filtered2['lastPrice_PE'].shift(+3))
    
   #Call butterfly 4 -------
    
    df_filtered2['btrfly_4'] = (df_filtered2['lastPrice_CE'] + df_filtered2['lastPrice_PE']) - (df_filtered2['lastPrice_CE'].shift(-4) + df_filtered2['lastPrice_PE'].shift(+4))
    
    
        
    
    
    
    
    

    column_order = ['expiryDate', 'underlying_CE', 'underlyingValue_CE', 'Strangle_2', 'Strangle_1', 'Straddles_1','Spread_3_C','Spread_2_C','Spread_1_C',
                    'lastPrice_CE', 'strikePrice', 'lastPrice_PE','Spread_1_P','Spread_2_P','Spread_3_P','btrfly_1','btrfly_2','btrfly_3','btrfly_4']
    df_filtered2 = df_filtered2[column_order].copy()

    return df_filtered2, unique_expiry_dates_formatted

# Sidebar
selected_symbol = st.sidebar.selectbox("#### Index ", options=("NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"))
st.session_state.selected_symbol = selected_symbol

# Main content
# Update df_filtered2 and unique_expiry_dates_formatted
df_filtered2, unique_expiry_dates_formatted = update_data()

selected_date = st.selectbox('#### Select Date', options=unique_expiry_dates_formatted)
if st.button("Refresh Data"):
    st.session_state.selected_date = selected_date

# Display df_filtered2
st.dataframe(df_filtered2)



















