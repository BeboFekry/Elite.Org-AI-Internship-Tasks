import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns

st.set_page_config(page_title='Dashboard', layout='wide')
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('data/retail_sales_cleaned.csv')
    st.session_state.df['Date'] = st.session_state.df['Date'].astype('datetime64[s]')

df = st.session_state.df

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Sales", f"{round(df['Sales'].sum(), 2)} :green[$]", border=True)
with col2:
    st.metric("Total Profits", f"{round(df['Profit'].sum(), 2)} :green[$]", border=True)
with col3:
    st.metric("Average Net Profit Percentage", f"{round((df['Profit'].sum()/df['Sales'].sum())*100, 2)} :green[%]", border=True)
with col4:
    st.metric("Number of Categories", len(df['Category'].unique()), border=True)
with col5:
    st.metric("Number of Regions", len(df['Region'].unique()), border=True)

with st.sidebar:
    st.subheader(":material/settings: Filters", divider='blue')

    category = st.selectbox("Category",["ALL"]+df['Category'].unique().tolist())
    if category and category!='ALL':
        df = df[df['Category']==category]
    region = st.selectbox("Region",["ALL"]+df['Region'].unique().tolist())
    if region and region!='ALL':
        df = df[df['Region']==region]

    
tab1, tab2 = st.tabs(['Features Analysis', 'Performace Analysis'])
with tab1:
    # st.header("Category Analysis", divider='blue')
    col1, col2 = st.columns([1,1.5])
    with col1:
        st.subheader("Selled Quanities for each category", width='content', divider='blue')
        insight = """Noticed that all selled products have approximately the same ratio, also the very near total value of sales, and very near profits as show in the next 3 figures.  
        \nAll categories are very near in the number of selled quantities but not the same profit, so we need to give more focus to market the product categories with the higher profits to increase the overall profits."""
        st.markdown(insight)
    with col2:
        # with st.container(border=True):
        d = df.groupby('Category')['Quantity'].sum().reset_index(name='Quantity')
        fig = px.pie(d,
            names='Category',
            values='Quantity',
            # title='Average Number of Dependents Ration beteen stayed and left emplyees',
            hole=0.3,
            )
        st.plotly_chart(fig)
    st.divider()
    st.subheader("Total Sales and Profit Values for each category", width='content', divider='blue')
    col1, col2 = st.columns([1,1])
    with col1:
        d = df.groupby('Category')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Category',
            y='Sales',
            title='Total Sales for each category',
            labels={'Category': 'Category', 'profit_percentage': 'Net Profit Percentage'},
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    with col2:
        d = df.groupby('Category')['Profit'].sum().reset_index(name='Profit')
        fig = px.bar(
            d, 
            x='Category',
            y='Profit',
            title='Total Profit for each category',
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    insight = """The highest total sales value is for "Books" followed by "Electronics".  \n"Books" is the top product these year, 
    it have the highest number of selled quantities and the highest sales value and also the highest profit value. There for we need to give some focus on books selling specially in South region"""
    st.markdown(insight)
    st.divider()


    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("Total Number of selled quantities in each Region", width='content', divider='blue')
        insight = """The highest Region sales is :green[South] followed by :green[North] by :green[~26\%] from total number of selled products for each,
        and the least Region in sales is :red[East] by :red[~22%], there is a problem in East region need to solve. """
        st.markdown(insight)
    with col2:
        d = df.groupby('Region')['Quantity'].sum().reset_index(name='Quantity')
        fig = px.pie(d,
            names='Region',
            values='Quantity',
            # title='Total Number of selled quantities in each Region',
            hole=0.3,
            )
        st.plotly_chart(fig)
    st.divider()

    st.subheader("Total Sales and Profit Values for each region", width='content', divider='blue')
    col1, col2 = st.columns(2)
    with col1:
        d = df.groupby('Region')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Region',
            y='Sales',
            title='Total sales for each Region',
            text_auto='.1f',
            color='Region'
        )
        st.plotly_chart(fig)
    with col2:
        d = df.groupby('Region')['Profit'].sum().reset_index(name='Profit')
        fig = px.bar(
            d, 
            x='Region',
            y='Profit',
            title='Total profits for each Region',
            text_auto='.1f',
            color='Region'
        )
        st.plotly_chart(fig)
    st.divider()

    st.subheader("Net Profit percentage for each Category and Region", width='content', divider='blue')

    col1, col2 = st.columns([1.2,1])
    with col1:
        d = (df.assign(profit_percentage=(df['Profit']/df['Sales']*100))
            .groupby('Category')['profit_percentage']
            .mean() 
            .reset_index(name='profit_percentage')
            )
        d['percent'] = d['profit_percentage'].apply(lambda x: f"{round(x, 2)} %")
        fig = px.bar(
            d, 
            x='Category',
            y='profit_percentage',
            title='Net profit percentage for each category',
            text='percent',
            labels={'Category': 'Category', 'profit_percentage': 'Net Profit Percentage'},
            # text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    with col2:
        d = (df.assign(profit_percentage=(df['Profit']/df['Sales']*100))
            .groupby('Region')['profit_percentage']
            .mean() 
            .reset_index(name='profit_percentage')
            )
        d['percent'] = d['profit_percentage'].apply(lambda x: f"{round(x, 2)} %")
        fig = px.bar(
            d, 
            x='Region',
            y='profit_percentage',
            title='Net profit percentage for each region',
            text='percent',
            labels={'Region': 'Region', 'profit_percentage': 'Net Profit Percentage'},
            # text_auto='.1f',
            color='Region'
        )
        st.plotly_chart(fig)
    st.markdown(f"""The Average Net Profit is :green[{round((df['Profit'].sum()/df['Sales'].sum())*100,2)} %]  \nThe highest category's profit is "Sports" products focusing in this category will increasing the total profit (Sports category is the top selling category in the West region), we can to increase marketing campains in the West region for the sports products""")
    st.divider()


with tab2:
    st.subheader("Total Sales over Days", width='content', divider='blue')
    d = df.groupby('Date')['Sales'].sum().reset_index(name='Daily Sales')
    fig = px.line(d, 
                x='Date', 
                y='Daily Sales', 
                template='plotly',
                labels={'week':'Week', 'metric_value':'Metric Value'}, 
                # title='Total Sales over Days'
                )
    st.plotly_chart(fig)
    d = df.groupby('Date')['Sales'].sum().reset_index(name='Daily Sales')
    fig = px.scatter(d, 
                x='Date', 
                y='Daily Sales', 
                template='plotly',
                labels={'Date':'Day', 'Daily Sales':'Total Sales per Month'}, 
                #   title='Total Sales over days'
                )
    st.plotly_chart(fig)
    st.divider()

    st.subheader("Total Sales over Months", width='content', divider='blue')
    d = df.copy()
    d['Date'] = d['Date'].apply(lambda x: x.month)
    # d = d.groupby(['Date','Category'])['Sales'].sum().reset_index(name='Daily Sales')
    d = d.groupby('Date')['Sales'].sum().reset_index(name='Daily Sales')
    fig = px.line(d, 
                x='Date', 
                y='Daily Sales', 
                template='plotly',
                labels={'Date':'Month', 'Daily Sales':'Total Sales per Month'}, 
                title='Total Sales over months',
                # color='Category',
    )
    st.plotly_chart(fig)
    st.divider()
    # ===============================================================================================
    st.subheader("""Total Sales over months for each separated region (:blue[North, South, East, and West]) regions""", width='content', divider='blue')
    col1, col2 = st.columns(2)
    
    st.subheader("Sales of :blue[North] Region", width='content', divider='blue')
    col1, col2 = st.columns([1,2])
    with col1:
        d = df[df['Region']=='North'].copy()
        d = d.groupby('Category')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Category',
            y='Sales',
            title='Total Sales for each category for North region',
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    with col2:
        d = df[df['Region']=='North'].copy()
        d['Date'] = d['Date'].apply(lambda x: x.month)
        d = d.groupby(['Date','Category'])['Sales'].sum().reset_index(name='Daily Sales')
        fig = px.line(d, 
                    x='Date', 
                    y='Daily Sales', 
                    template='plotly',
                    labels={'Date':'Month', 'Daily Sales':'Total Sales per Month'}, color='Category',
                    title='Total Sales over months for "North" region only')
        st.plotly_chart(fig)
    insight = """**At North Region**  \nThe highest pay rate category is :red[Clothing] with total sales 100k and highest month's sales 13.5k at October (the start of the winter new collection clothing season) and second highest month's sales is 11.5k at May (the start of the summer new collection clothing season). There for we can to focus on the clothing merketing campains at months April and May, then at September and October. 
    \nThe 2nd highest sales rate category is :blue[Books] with 95k total sales and highest month's sales of 12.5k at May (the starting of ther summer vacation), and also all other categories's sales increases starting from May, There for we can to make a comprehensive merketing campains at months April, May, and June"""
    st.markdown(insight)
    st.divider()


    st.subheader("Sales of :blue[South] Region", width='content', divider='blue')
    col1, col2 = st.columns([1,2])
    with col1:
        d = df[df['Region']=='South'].copy()
        d = d.groupby('Category')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Category',
            y='Sales',
            title='Total Sales for each category for South region',
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    with col2:
        d = df[df['Region']=='South'].copy()
        d['Date'] = d['Date'].apply(lambda x: x.month)
        d = d.groupby(['Date','Category'])['Sales'].sum().reset_index(name='Daily Sales')

        fig = px.line(d, 
                    x='Date', 
                    y='Daily Sales', 
                    template='plotly',
                    labels={'Date':'Month', 'Daily Sales':'Total Sales per Month'}, color='Category',
                    title='Total Sales over months for "South" region only')
        st.plotly_chart(fig)
    insight = """**At South Region**  \nThe highest pay rate category is :blue[Books], :green[Electronics] and :red[Clothing] with total sales 97.2k, 96.5k and 95.8k and highest month's sales 12.6k at February for Books and November for Clothing.  \nSo we need to increase marketing campains focusing on books at February and September,focusing on Clothing at November and focusing on Electronics at December"""
    st.markdown(insight)
    st.divider()

    
    st.subheader("Sales of :blue[East] Region", width='content', divider='blue')
    col1, col2 = st.columns([1,2])
    with col1:
        d = df[df['Region']=='East'].copy()
        d = d.groupby('Category')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Category',
            y='Sales',
            title='Total Sales for each category for East region',
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig)
    with col2:
        d = df[df['Region']=='East'].copy()
        d['Date'] = d['Date'].apply(lambda x: x.month)
        d = d.groupby(['Date','Category'])['Sales'].sum().reset_index(name='Daily Sales')
        fig = px.line(d, 
            x='Date', 
            y='Daily Sales', 
            template='plotly',
            labels={'Date':'Month', 'Daily Sales':'Total Sales per Month'}, color='Category',
            title='Total Sales over months for "East" region only')
        st.plotly_chart(fig)
    insight = """**At East Region**  \nThe highest pay rate category is :violet[Home Goods] and :blue[Books] with total sales 82k and 80k and highest month's sales 11k at June for Books and 10.5 for Home Goods at October.  \nSo i recommend to increase marketing campains focusing on Home Goods at (July and October) and focusing on Books at June."""
    st.markdown(insight)
    st.divider()



    st.subheader("Sales of :blue[West] Region", width='content', divider='blue')
    col1, col2 = st.columns([1,2])
    with col1:
        d = df[df['Region']=='West'].copy()
        d = d.groupby('Category')['Sales'].sum().reset_index(name='Sales')
        fig = px.bar(
            d, 
            x='Category',
            y='Sales',
            title='Total Sales for each category for West region',
            text_auto='.1f',
            color='Category'
        )
        st.plotly_chart(fig, key=555)
    with col2:
        d = df[df['Region']=='West'].copy()
        d['Date'] = d['Date'].apply(lambda x: x.month)
        d = d.groupby(['Date','Category'])['Sales'].sum().reset_index(name='Daily Sales')
        fig = px.line(d, 
            x='Date', 
            y='Daily Sales', 
            template='plotly',
            labels={'Date':'Month', 'Daily Sales':'Total Sales per Month'}, color='Category',
            title='Total Sales over months for "West" region only')
        st.plotly_chart(fig)
    insight = """**At East Region**  \nThe highest pay rate category is :green[Electronics] and :orange[Sports] with total sales 100k and 98k and highest month's sales 13.8k at December for Electronics and 14.6k for Sports at October.  \nSo i recommend to increase marketing campains focusing on Electronics at (December) and focusing on Sport products at October."""
    st.markdown(insight)
    st.divider()    


