from numbers import Number
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import simfin as sf

sf.set_data_dir('~/simfin_data/')
sf.set_api_key(api_key = st.secrets['key'])

st.set_page_config(layout="wide")

with st.spinner('Wait for it...'):

    hub = sf.StockHub(market='us',
        refresh_days=30,
        refresh_days_shareprices=1)

    hub = sf.StockHub(market='us',
        refresh_days=30,
        refresh_days_shareprices=1)

    @st.cache
    def load_val_data():
        df_val_signals = hub.val_signals(variant='latest')
        return df_val_signals

    @st.cache
    def load_growth_data():
        df_growth_signals = hub.growth_signals(variant='latest')
        return df_growth_signals

    @st.cache
    def load_fin_data():
        df_fin_signals = hub.fin_signals(variant='latest')
        return df_fin_signals

    @st.cache
    def load_company_names():
            df_company_names = sf.load_companies(market='us')
            return df_company_names

    df_val_signals = load_val_data()
    df_growth_signals = load_growth_data()
    df_fin_signals = load_fin_data()
    df_company_names = load_company_names()

    dfs = [df_fin_signals, df_growth_signals, df_val_signals]
    df_signals = pd.concat(dfs, axis=1)
    #df_signals.to_excel(r"C:\Users\Tom\OneDrive\Documenten\df signals.xlsx")
    df_signals = df_signals.reset_index()

    tickers = df_signals ['Ticker']
    names = []

    for t in tickers:
            company_names = df_company_names.loc [t] ['Company Name']

            names.append (company_names)

    company_names = pd.DataFrame(names)

    company_names.columns = ['Company Name']

    dfs = [df_signals, company_names]
    df_signals = pd.concat(dfs, axis=1)
    #df_signals.to_excel(r'C:\Users\Tom\OneDrive\Documenten\lijst met tickers.xlsx')
    # Show the result.
    #df_signals = df_signals.set_index('Ticker')
    df_val_signals = df_val_signals.sort_values('Market-Cap', ascending=False)
    #df_val_signals = df_val_signals [['Ticker', 'Market-Cap', 'Dividend Yield', 'P/E' , 'P/Sales', 'Price to Book Value' ,'P/FCF']]
    df_val_signals = df_val_signals.round({'P/E': 1, 'P/Sales': 1, 'Price to Book Value': 1, 'P/FCF': 1})


    #df_signals = df_signals.replace(np.nan, '0')
    df_signals = df_signals.sort_values('Market-Cap', ascending=False)
    df_signals = df_signals.round(3)

    #df_overview = df_signals [['Ticker', 'Company Name', 'Market-Cap', 'P/E', 'Dividend Yield']]
    df_value= df_signals [['Ticker', 'Company Name', 'Market-Cap', 'P/E', 'P/FCF', 'P/Sales', 'P/NetNet', 'Price to Book Value', 'P/Cash']]
    df_growth = df_signals [['Ticker', 'Company Name', 'Market-Cap', 'Return on Assets', 'Return on Equity', 'Earnings Growth', 'Sales Growth', 'FCF Growth', 'Assets Growth']]
    df_financials =df_signals[['Ticker', 'Company Name', 'Market-Cap', 'Current Ratio', 'Debt Ratio', 'Gross Profit Margin', 'Interest Coverage', 'Asset Turnover', 'Inventory Turnover']]
    df_val_signals['P/Sales'] = df_val_signals['P/Sales'].astype(np.float64)
    df_val_signals['Dividend Yield'] = df_val_signals['Dividend Yield'].astype(np.float64)
    #df[df['Dividend Yield']<0 ] = 0

    tab1, tab2, tab3, tab4 = st.tabs(["Basic filter options", "Value filter options", "Growth filter options", "Financials filter options"])

    with tab2:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col6:
            min_pcash = st.selectbox('P/Cash',
                ['Min P/Cash', 0.1, 0.5, 1, 5, 10, 15, 20])
            max_pcash = st.selectbox('',
                ['Max P/Cash', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]) 


        with col1:
            min_pe = st.selectbox('P/E Ratio',
                ['Min P/E Ratio', 0.1, 0.5, 1, 5, 10, 15, 20])
        with col1:
            max_pe = st.selectbox('',
                ['Max P/E Ratio', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

        with col3:
            min_sales = st.selectbox('P/Sales Ratio',
                ['Min P/Sales Ratio', 0.1, 0.5, 1, 5, 10, 15, 20])
        with col3:
            max_sales = st.selectbox('',
                ['Max P/Sales Ratio', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

        with col2:
            min_fcf = st.selectbox('P/FCF Ratio',
                ['Min P/FCF', 0.1, 0.5, 1, 5, 10, 15, 20])
        with col2:
            max_fcf = st.selectbox('',
                ['Max P/FCF', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

        with col4:
            min_netnet = st.selectbox('P/NetNet',
                ['Min P/NetNet', 0.1, 0.5, 1, 5, 10, 15, 20])
        with col4:
            max_netnet = st.selectbox('',
                ['Max P/NetNet', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

        with col5:
            min_ptb = st.selectbox('Price to book value',
                ['Min Price to book value', 0.1, 0.5, 1, 5, 10, 15, 20])
        with col5:
            max_ptb = st.selectbox('',
                ['Max Price to book value', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])




    with tab3:
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                    min_roa= st.number_input('Min Return on assets')   
                    max_roa= st.number_input('Max Return on assets')   

            with col2:
                    min_roe= st.number_input('Min Return on equity')   
                    max_roe = st.number_input('Max Return on equity')

            with col3:
                    min_eg= st.number_input('Min Earnings growth')   
                    max_eg = st.number_input('Max Earnings growth')

            with col4:
                    min_sg= st.number_input('Min Sales growth')   
                    max_sg = st.number_input('Max Sales growth')

            with col5:
                    min_fcfg= st.number_input('Min FCF growth')   
                    max_fcfg = st.number_input('Max FCF growth')

            with col6:
                    min_assets= st.number_input('Min Assets growth')   
                    max_assets = st.number_input('Max Assets growth')

    with tab4:

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                    min_current= st.number_input('Min Current ratio')   
                    max_current = st.number_input('Max Current ratio') 

            with col2:
                    min_debt= st.number_input('Min Debt ratio')   
                    max_debt = st.number_input('Max Debt ratio')

            with col3:
                    min_pmargin= st.number_input('Min Gross profit margin')   
                    max_pmargin = st.number_input('Max Gross profit margin')

            with col4:
                    min_ic= st.number_input('Min Interest coverage')   
                    max_ic = st.number_input('Max Interest coverage')

            with col5:
                    min_at= st.number_input('Min Asset turnover')   
                    max_at = st.number_input('Max Asset turnover')

            with col6:
                    min_it= st.number_input('Min Inventory turnover')   
                    max_it = st.number_input('Max Inventory turnover')    





    with tab2:
            st.markdown("""---""")
    with tab3:
            st.markdown("""---""")
    with tab4:
            st.markdown("""---""")


    col1,col2 = st.columns([1,4])
    with col1:
            sort = st.selectbox('Sort on...',
            ('Market-Cap', 'Dividend Yield', 'P/E', 'P/Sales', 'Price to Book Value', 'P/FCF'))

            selectdf = st.radio(
            "Select view",
            ('Overview', 'Value', 'Growth', 'Financials'))

            min_market_cap, max_market_cap = st.select_slider('Select market cap range',options=['min', '100m', '500m', '1b', '5b', '20b', '50b', '100b', '200b', '500b', 'max'], value=('min', 'max'))
            min_dividend, max_dividend = st.slider('Select dividend yield range (%)',0.0, 10.0, (0.0, 10.0), step=0.1)



    if sort=='Market-Cap':
                df_signals=df_signals
    if sort=='Dividend Yield':
                df_signals = df_signals.sort_values('Dividend Yield', ascending=False)
    if sort=='P/E':
                df_signals = df_signals.sort_values('P/E', ascending=True)
    if sort=='P/Sales':
                df_signals = df_signals.sort_values('P/Sales', ascending=True) 
    if sort=='Price to Book Value':
                df_signals = df_signals.sort_values('Price to Book Value', ascending=True)
    if sort=='P/FCF':
                df_signals = df_signals.sort_values('P/FCF', ascending=True)

    if max_market_cap=='500b':
                df_mask = df_signals ['Market-Cap']< 500000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='200b':
                df_mask = df_signals ['Market-Cap']< 200000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='100b':
                df_mask = df_signals ['Market-Cap']< 100000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='50b':
                df_mask = df_signals ['Market-Cap']< 50000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='20b':
                df_mask = df_signals ['Market-Cap']< 20000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='5b':
                df_mask = df_signals ['Market-Cap']< 5000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='1b':
                df_mask = df_signals ['Market-Cap']< 1000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='500m':
                df_mask = df_signals ['Market-Cap']< 500000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if max_market_cap=='100m':
                df_mask = df_signals ['Market-Cap']< 100000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]


    if min_market_cap=='500b':
                df_mask = df_signals ['Market-Cap']> 500000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='200b':
                df_mask = df_signals ['Market-Cap']> 200000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='100b':
                df_mask = df_signals ['Market-Cap']> 100000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='50b':
                df_mask = df_signals ['Market-Cap']> 50000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='20b':
                df_mask = df_signals ['Market-Cap']> 20000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='5b':
                df_mask = df_signals ['Market-Cap']> 5000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='1b':
                df_mask = df_signals ['Market-Cap']> 1000000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    if min_market_cap=='500m':
                df_mask = df_signals ['Market-Cap']> 500000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]


    if min_market_cap=='100m':
                df_mask = df_signals ['Market-Cap']> 100000000
                positions = np.flatnonzero(df_mask)
                df_signals=df_signals.iloc[positions]

    df_signals['Dividend Yield'] = df_signals['Dividend Yield'].fillna(0)


    mask = df_signals ['Dividend Yield']>= min_dividend/100
    df_signals = df_signals [mask]

    mask = df_signals ['Dividend Yield']<= max_dividend/100
    df_signals = df_signals [mask]

    if min_pe != 'Min P/E Ratio':
            df_mask = df_signals ['P/E']> min_pe
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_pe != 'Max P/E Ratio':
            df_mask = df_signals ['P/E']< max_pe
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_sales != 'Min P/Sales Ratio':
            df_mask = df_signals ['P/Sales']> min_sales
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_sales != 'Max P/Sales Ratio':
            df_mask = df_signals ['P/Sales']< max_sales
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]    

    if min_ptb != 'Min Price to book value':
            df_mask = df_signals ['Price to Book Value']> min_ptb
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_ptb != 'Max Price to book value':
            df_mask = df_signals ['Price to Book Value']< max_ptb
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]  

    if min_fcf != 'Min P/FCF':
            df_mask = df_signals ['P/FCF']> min_fcf
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_fcf != 'Max P/FCF':
            df_mask = df_signals ['P/FCF']< max_fcf
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_netnet != 'Min P/NetNet':
            df_mask = df_signals ['P/NetNet']> min_netnet
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_netnet != 'Max P/NetNet':
            df_mask = df_signals ['P/NetNet']< max_netnet
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_pcash != 'Min P/Cash':
            df_mask = df_signals ['P/Cash']> min_pcash
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_pcash != 'Max P/Cash':
            df_mask = df_signals ['P/Cash']< max_pcash
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]


    if min_roa != 0:
            df_mask = df_signals ['Return on Assets']> min_roa
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_roa != 0:
            df_mask = df_signals ['Return on Assets']< max_roa
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_roe != 0:
            df_mask = df_signals ['Return on Equity']> min_roe
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_roe != 0:
            df_mask = df_signals ['Return on Equity']< max_roe
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_eg != 0:
            df_mask = df_signals ['Earnings Growth']> min_eg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_eg != 0:
            df_mask = df_signals ['Earnings Growth']< max_eg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_sg != 0:
            df_mask = df_signals ['Sales Growth']> min_sg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_sg != 0:
            df_mask = df_signals ['Sales Growth']< max_sg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_fcfg != 0:
            df_mask = df_signals ['FCF Growth']> min_fcfg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_fcfg != 0:
            df_mask = df_signals ['FCF Growth']< max_fcfg
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_assets != 0:
            df_mask = df_signals ['Assets Growth']> min_assets
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_assets != 0:
            df_mask = df_signals ['Assets Growth']< max_assets
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_current != 0:
            df_mask = df_signals ['Current Ratio']> min_current
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_current != 0:
            df_mask = df_signals ['Current Ratio']< max_current
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_debt != 0:
            df_mask = df_signals ['Debt Ratio']> min_debt
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_debt != 0:
            df_mask = df_signals ['Debt Ratio']< max_debt
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_pmargin != 0:
            df_mask = df_signals ['Gross Profit Margin']> min_pmargin
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_pmargin != 0:
            df_mask = df_signals ['Gross Profit Margin']< max_pmargin
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_ic != 0:
            df_mask = df_signals ['Interest Coverage']> min_ic
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_ic != 0:
            df_mask = df_signals ['Interest Coverage']< max_ic
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_at != 0:
            df_mask = df_signals ['Asset Turnover']> min_at
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_at != 0:
            df_mask = df_signals ['Asset Turnover']< max_at
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if min_it != 0:
            df_mask = df_signals ['Inventory Turnover']> min_it
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]

    if max_it != 0:
            df_mask = df_signals ['Inventory Turnover']< max_it
            positions = np.flatnonzero(df_mask)
            df_signals=df_signals.iloc[positions]










    if selectdf == 'Overview':

     with col2:


        cell_renderer = JsCode("""
            function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
            """)

        df_signals = df_signals [['Ticker', 'Company Name', 'Market-Cap', 'P/E', 'Dividend Yield']]


        df_signals.loc[:, "Market-Cap"] = df_signals["Market-Cap"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/E"] = df_signals["P/E"].map('{:,.2f}'.format)


        df_signals.loc[:, "Dividend Yield"] =df_signals["Dividend Yield"].map('{:.1%}'.format)
        df_signals = df_signals.replace({'nan%': '-'})


        gd = GridOptionsBuilder.from_dataframe(df_signals)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column (min_column_width= 100, filterable=False, sorteable=False, header=False, type=['leftAligned'])

        gd.configure_column("Ticker", cellRenderer=cell_renderer)

        #gd.configure_column('P/Sales', type=['rightAligned'])
        #gd.configure_column('Price to Book Value', type=['rightAligned'])
        #gd.configure_column('P/FCF', type=['rightAligned'])

        gridoptions = gd.build()

        grid_table = AgGrid(df_signals,
                gridOptions=gridoptions, 
                height= 640,
                width= '150%',
                theme= 'material',
                alignment= 'centered',
                allow_unsafe_jscode=True
                )


    ##############################
    if selectdf == 'Value':
     with col2:
        df_signals = df_signals [['Ticker', 'Company Name', 'Market-Cap', 'P/E', 'P/FCF', 'P/Sales', 'P/NetNet', 'Price to Book Value', 'P/Cash']]



        if sort=='Market-Cap':
                df_signals=df_signals
        if sort=='Dividend Yield':
                df_signals = df_signals.sort_values('Dividend Yield', ascending=False)
        if sort=='P/E':
                df_signals = df_signals.sort_values('P/E', ascending=True)
        if sort=='P/Sales':
                df_signals = df_signals.sort_values('P/Sales', ascending=True) 
        if sort=='Price to Book Value':
                df_signals = df_signals.sort_values('Price to Book Value', ascending=True)
        if sort=='P/FCF':
                df_signals = df_signals.sort_values('P/FCF', ascending=True)



        cell_renderer = JsCode("""
            function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
            """)


        df_signals.loc[:, "Market-Cap"] = df_signals["Market-Cap"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/E"] = df_signals["P/E"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/Sales"] = df_signals["P/Sales"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/FCF"] = df_signals["P/FCF"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/NetNet"] = df_signals["P/NetNet"].map('{:,.2f}'.format)
        df_signals.loc[:, "Price to Book Value"] = df_signals["Price to Book Value"].map('{:,.2f}'.format)
        df_signals.loc[:, "P/Cash"] = df_signals["P/Cash"].map('{:,.2f}'.format)
        #data.loc[:, "Dividend Yield"] =data["Dividend Yield"].map('{:.1%}'.format)
        df_signals = df_signals.replace({'nan': '-'})


        gd = GridOptionsBuilder.from_dataframe(df_signals)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column (min_column_width= 100, filterable=False, sorteable=False, header=False, type=['leftAligned'])

        gd.configure_column("Ticker", cellRenderer=cell_renderer)


        gridoptions = gd.build()

        grid_table = AgGrid(df_signals,
                gridOptions=gridoptions, 
                height= 640,
                width= '100%',
                theme= 'material',
                alignment= 'centered',
                allow_unsafe_jscode=True
                )

    if selectdf == 'Growth':
       with col2:   
        df_signals = df_signals [['Ticker', 'Company Name', 'Market-Cap', 'Return on Assets', 'Return on Equity', 'Earnings Growth', 'Sales Growth', 'FCF Growth', 'Assets Growth']]


        if sort=='Market-Cap':
                df_signals=df_signals
        if sort=='Dividend Yield':
                df_signals = df_signals.sort_values('Dividend Yield', ascending=False)
        if sort=='P/E':
                df_signals = df_signals.sort_values('P/E', ascending=True)
        if sort=='P/Sales':
                df_signals = df_signals.sort_values('P/Sales', ascending=True) 
        if sort=='Price to Book Value':
                df_signals = df_signals.sort_values('Price to Book Value', ascending=True)
        if sort=='P/FCF':
                df_signals = df_signals.sort_values('P/FCF', ascending=True)  

        cell_renderer = JsCode("""
            function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
            """)

        df_signals.loc[:, "Market-Cap"] = df_signals["Market-Cap"].map('{:,.2f}'.format)
        df_signals.loc[:, "Return on Assets"] = df_signals["Return on Assets"].map('{:,.2f}'.format)
        df_signals.loc[:, "Return on Equity"] = df_signals["Return on Equity"].map('{:,.2f}'.format)
        df_signals.loc[:, "Earnings Growth"] = df_signals["Earnings Growth"].map('{:,.2f}'.format)
        df_signals.loc[:, "Sales Growth"] = df_signals["Sales Growth"].map('{:,.2f}'.format)
        df_signals.loc[:, "FCF Growth"] = df_signals["FCF Growth"].map('{:,.2f}'.format)
        df_signals.loc[:, "Assets Growth"] = df_signals["Assets Growth"].map('{:,.2f}'.format)

        #data.loc[:, "Dividend Yield"] =data["Dividend Yield"].map('{:.1%}'.format)
        #data = data.replace({'nan%': '-'})

        gd = GridOptionsBuilder.from_dataframe(df_signals)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column (min_column_width= 100, filterable=False, sorteable=False, header=False, type=['leftAligned'])

        gd.configure_column("Ticker", cellRenderer=cell_renderer)
        #gd.configure_column('Dividend Yield', type=['rightAligned'])


        gridoptions = gd.build()

        grid_table = AgGrid(df_signals,
                gridOptions=gridoptions, 
                height= 640,
                width= '100%',
                theme= 'material',
                alignment= 'centered',
                allow_unsafe_jscode=True
                )

    if selectdf == 'Financials':
     with col2:    
        df_signals = df_signals[['Ticker', 'Company Name', 'Market-Cap', 'Current Ratio', 'Debt Ratio', 'Gross Profit Margin', 'Interest Coverage', 'Asset Turnover', 'Inventory Turnover']]

        if sort=='Market-Cap':
                df_signals=df_signals
        if sort=='Dividend Yield':
                df_signals = df_signals.sort_values('Dividend Yield', ascending=False)
        if sort=='P/E':
                df_signals = df_signals.sort_values('P/E', ascending=True)
        if sort=='P/Sales':
                df_signals = df_signals.sort_values('P/Sales', ascending=True) 
        if sort=='Price to Book Value':
                df_signals = df_signals.sort_values('Price to Book Value', ascending=True)
        if sort=='P/FCF':
                df_signals = df_signals.sort_values('P/FCF', ascending=True)

        cell_renderer = JsCode("""
            function(params) {return `<a href="https://www.investcroc.com/${params.value}" target="_blank">${params.value}</a>`}
            """)


        df_signals.loc[:, "Market-Cap"] = df_signals["Market-Cap"].map('{:,.2f}'.format)
        df_signals.loc[:, "Current Ratio"] = df_signals["Current Ratio"].map('{:,.2f}'.format)
        df_signals.loc[:, "Debt Ratio"] = df_signals["Debt Ratio"].map('{:,.2f}'.format)
        df_signals.loc[:, "Gross Profit Margin"] = df_signals["Gross Profit Margin"].map('{:,.2f}'.format)
        df_signals.loc[:, "Interest Coverage"] = df_signals["Interest Coverage"].map('{:,.2f}'.format)
        df_signals.loc[:, "Asset Turnover"] = df_signals["Asset Turnover"].map('{:,.2f}'.format)
        df_signals.loc[:, "Inventory Turnover"] = df_signals["Inventory Turnover"].map('{:,.2f}'.format)
        #data.loc[:, "Dividend Yield"] =data["Dividend Yield"].map('{:.1%}'.format)
        df_signals = df_signals.replace({'nan': '-'})


        gd = GridOptionsBuilder.from_dataframe(df_signals)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column (min_column_width= 100, filterable=False, sorteable=False, header=False, type=['leftAligned'])

        gd.configure_column("Ticker", cellRenderer=cell_renderer)


        gridoptions = gd.build()

        grid_table = AgGrid(df_signals,
                gridOptions=gridoptions, 
                height= 640,
                width= '100%',
                theme= 'material',
                alignment= 'centered',
                allow_unsafe_jscode=True
                )
