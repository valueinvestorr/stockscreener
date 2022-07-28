from numbers import Number
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import simfin as sf

sf.set_data_dir('~/simfin_data/')
sf.set_api_key(api_key = st.secrets['key'])

st.set_page_config(layout="wide")

hub = sf.StockHub(market='us',
    refresh_days=30,
    refresh_days_shareprices=1)

@st.cache
def load_data():
    df_val_signals = hub.val_signals(variant='latest')
    return df_val_signals
    
df_val_signals = load_data()
df_val_signals = df_val_signals.reset_index()

df_val_signals = df_val_signals.sort_values('Market-Cap', ascending=False)
df_val_signals = df_val_signals [['Ticker', 'Market-Cap', 'Dividend Yield', 'P/E' , 'P/Sales', 'Price to Book Value' ,'P/FCF']]
df_val_signals = df_val_signals.round({'P/E': 1, 'Dividend Yield': 3, 'P/Sales': 1, 'Price to Book Value': 1, 'P/FCF': 1})
df = df_val_signals
df['Market-Cap'] = df['Market-Cap'].astype(np.float64)

df_mask = df ['Market-Cap']> 10
positions = np.flatnonzero(df_mask)
filtered_df=df.iloc[positions]

df_val_signals = df_val_signals.replace(np.nan, '0')

df_val_signals['P/Sales'] = df_val_signals['P/Sales'].astype(np.float64)
df_val_signals['Dividend Yield'] = df_val_signals['Dividend Yield'].astype(np.float64)
df[df['Dividend Yield']<0 ] = 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    sort = st.selectbox('Sort on...',
     ('Market-Cap', 'Dividend Yield', 'P/E', 'P/Sales', 'Price to Book Value', 'P/FCF'))
with col2:
    select = st.select_slider('Market-Cap',options=['<100m', '<500m', '<1b', '<5b', '<20b', '<50b', '<100b', '<200b', '<500b', 'max'], value='max')

##############################
agree = st.checkbox('Show filter options')

if agree:
     

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        min_dividend = st.selectbox('Dividend Yield', 
        ['Min dividend yield (%)', 0.1, 0.2, 0.5, 1, 1.5, 2.5, 3, 4, 5])

    with col2:
        min_pe = st.selectbox('P/E Ratio',
            ['Min P/E Ratio', 0.1, 0.5, 1, 5, 10, 15, 20])

    with col3:
        min_sales = st.selectbox('P/Sales Ratio',
            ['Min P/Sales Ratio', 0.1, 0.5, 1, 5, 10, 15, 20])

    with col4:
        min_pb = st.selectbox('Price to book',
            ['Min price to book value', 0.1, 0.5, 1, 5, 10, 15, 20])  

    with col5:
        min_fcf = st.selectbox('P/FCF Ratio',
            ['Min P/FCF', 0.1, 0.5, 1, 5, 10, 15, 20])              

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        max_dividend = st.selectbox ('',
        ['Max dividend yield (%)', 0.1, 0.2, 0.5, 1, 2, 3, 4, 5, 10])

    with col2:
        max_pe = st.selectbox('',
            ['Max P/E Ratio', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    with col3:
        max_sales = st.selectbox('',
            ['Max P/Sales Ratio', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    with col4:
        max_pb = st.selectbox('',
            ['Max price to book value', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])  
    
    with col5:
        max_fcf = st.selectbox('',
            ['Max P/FCF', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])  

    data = df

    if min_dividend != 'Min dividend yield (%)':
        df_mask = data ['Dividend Yield']> min_dividend/100
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if max_dividend != 'Max dividend yield (%)':
        df_mask = data ['Dividend Yield']< max_dividend/100
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if min_pe != 'Min P/E Ratio':
        df_mask = data ['P/E']> min_pe
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if max_pe != 'Max P/E Ratio':
        df_mask = data ['P/E']< max_pe
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if min_sales != 'Min P/Sales Ratio':
        df_mask = data ['P/Sales']> min_sales
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if max_sales != 'Max P/Sales Ratio':
        df_mask = data ['P/Sales']< max_sales
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]    

    if min_pb != 'Min price to book value':
        df_mask = data ['Price to Book Value']> min_pb
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if max_pb != 'Max price to book value':
        df_mask = data ['Price to Book Value']< max_pb
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]  

    if min_fcf != 'Min P/FCF':
        df_mask = data ['P/FCF']> min_fcf
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if max_fcf != 'Max P/FCF':
        df_mask = data ['P/FCF']< max_fcf
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

        
    if select=='<500b':
            df_mask = data ['Market-Cap']< 500000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<200b':
            df_mask = data ['Market-Cap']< 200000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<100b':
            df_mask = data ['Market-Cap']< 100000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<50b':
            df_mask = data ['Market-Cap']< 50000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<20b':
            df_mask = data ['Market-Cap']< 20000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<5b':
            df_mask = data ['Market-Cap']< 5000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<1b':
            df_mask = data ['Market-Cap']< 1000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<500m':
            df_mask = data ['Market-Cap']< 500000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<100m':
            df_mask = data ['Market-Cap']< 100000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if sort=='Market-Cap':
            data= data  
    if sort=='Dividend Yield':
            data = data.sort_values('Dividend Yield', ascending=False)
    if sort=='P/E':
            data = data.sort_values('P/E', ascending=True)
    if sort=='P/Sales':
            data = data.sort_values('P/Sales', ascending=True) 
    if sort=='Price to Book Value':
            data = data.sort_values('Price to Book Value', ascending=True)
    if sort=='P/FCF':
            data = data.sort_values('P/FCF', ascending=True)  

    cell_renderer = JsCode("""
        function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
        """)

    data.loc[:, "Market-Cap"] = data["Market-Cap"].map('{:,.2f}'.format)
    data.loc[:, "Dividend Yield"] =data["Dividend Yield"].map('{:.1%}'.format)
    data = data.replace({'nan%': '-'})


    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_column("Ticker", cellRenderer=cell_renderer)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column (min_column_width= 180, filterable=False, sorteable=False, header=False)

    gd.configure_column('Dividend Yield', type=['rightAligned'])
    gd.configure_column('Market-Cap', type=['rightAligned'])
    gd.configure_column('P/E', type=['rightAligned'])
    gd.configure_column('P/Sales', type=['rightAligned'])
    gd.configure_column('Price to Book Value', type=['rightAligned'])
    gd.configure_column('P/FCF', type=['rightAligned'])

    gridoptions = gd.build()

    grid_table = AgGrid(data,
            gridOptions=gridoptions,
            height= 640,
            width= '150%',
            theme= 'material',
            alignment= 'centered',
            allow_unsafe_jscode=True
            )

else:

    data = df

    if select=='<500b':
        df_mask = data ['Market-Cap']< 500000000000
        positions = np.flatnonzero(df_mask)
        data=data.iloc[positions]

    if select=='<200b':
            df_mask = data ['Market-Cap']< 200000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<100b':
            df_mask = data ['Market-Cap']< 100000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<50b':
            df_mask = data ['Market-Cap']< 50000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<20b':
            df_mask = data ['Market-Cap']< 20000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<5b':
            df_mask = data ['Market-Cap']< 5000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<1b':
            df_mask = data ['Market-Cap']< 1000000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<500m':
            df_mask = data ['Market-Cap']< 500000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]

    if select=='<100m':
            df_mask = data ['Market-Cap']< 100000000
            positions = np.flatnonzero(df_mask)
            data=data.iloc[positions]
                        
    if sort=='Market-Cap':
            data= data  
    if sort=='Dividend Yield':
            data = data.sort_values('Dividend Yield', ascending=False)
    if sort=='P/E':
            data = data.sort_values('P/E', ascending=True)
    if sort=='P/Sales':
            data = data.sort_values('P/Sales', ascending=True) 
    if sort=='Price to Book Value':
            data = data.sort_values('Price to Book Value', ascending=True)
    if sort=='P/FCF':
            data = data.sort_values('P/FCF', ascending=True)  

    cell_renderer = JsCode("""
        function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
        """)

    data.loc[:, "Market-Cap"] = data["Market-Cap"].map('{:,.2f}'.format)
    data.loc[:, "Dividend Yield"] =data["Dividend Yield"].map('{:.1%}'.format)
    data = data.replace({'nan%': '-'})


    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_column("Ticker", cellRenderer=cell_renderer)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column (min_column_width= 180, filterable=False, sorteable=False, header=False)

    gd.configure_column('Dividend Yield', type=['rightAligned'])
    gd.configure_column('Market-Cap', type=['rightAligned'])
    gd.configure_column('P/E', type=['rightAligned'])
    gd.configure_column('P/Sales', type=['rightAligned'])
    gd.configure_column('Price to Book Value', type=['rightAligned'])
    gd.configure_column('P/FCF', type=['rightAligned'])

    gridoptions = gd.build()

    grid_table = AgGrid(data,
            gridOptions=gridoptions,
            height= 640,
            width= '150%',
            theme= 'material',
            alignment= 'centered',
            allow_unsafe_jscode=True
            )