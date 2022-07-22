import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import simfin as sf

sf.set_data_dir('~/simfin_data/')
sf.set_api_key(api_key = key)

st.set_page_config(layout="wide")
st. markdown("<h1 style='text-align: center;'>Stockscreener</h1>", unsafe_allow_html=True)

hub = sf.StockHub(market='us',
    refresh_days=30,
    refresh_days_shareprices=1)

df_val_signals = hub.val_signals(variant='latest')
df_val_signals = df_val_signals.reset_index()

df_val_signals = df_val_signals.sort_values('Market-Cap', ascending=False)
df_val_signals = df_val_signals [['Ticker', 'Market-Cap', 'Dividend Yield', 'P/E' , 'P/Sales', 'Price to Book Value' ,'P/FCF']]
df_val_signals = df_val_signals.round({'P/E': 1, 'Dividend Yield': 3, 'P/Sales': 1, 'Price to Book Value': 1, 'P/FCF': 1})
df_val_signals.dropna(subset=['Market-Cap'], inplace=True)
df_val_signals[df_val_signals['Dividend Yield']<0 ] = 0
df_val_signals[df_val_signals['Dividend Yield']<-0 ] = 0



#df_val_signals.loc[:, "Dividend Yield"] =df_val_signals["Dividend Yield"].map('{:.1%}'.format)
#df_val_signals.loc[:, "Market-Cap (in millions)"] = df_val_signals["Market-Cap (in millions)"].map('{:,.0f}'.format)
#df_val_signals = df_val_signals.replace({'nan%': '0'})
#df_val_signals = df_val_signals.replace(np.nan, '-')
#df_val_signals = df_val_signals.replace(np.inf, '-')
df_val_signals['P/Sales'] = df_val_signals['P/Sales'].astype(np.float64)
df_val_signals['Dividend Yield'] = df_val_signals['Dividend Yield'].astype(np.float64)

data = df_val_signals

gd = GridOptionsBuilder.from_dataframe(data)
gd.configure_pagination(enabled=True)
gd.configure_default_column (min_column_width= 190, alignment= 'right')

#sel_mode = st.radio('Selection Type', options= ['single', 'multiple'])
#gd.configure_selection (selection_mode=sel_mode, use_checkbox=True)
#gd.configure_columns (resizable=False)
gridoptions = gd.build()
grid_table = AgGrid(data, 
    gridOptions=gridoptions,
    height= 640,
    width= '150%',
    theme= 'material',
    alignment= 'centered',
    )

#df_val_signals['P/Sales'] = df_val_signals['P/Sales'].astype(int)


print(df_val_signals.dtypes)

