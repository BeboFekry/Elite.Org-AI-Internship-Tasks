import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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
        \nThere for we need to focus in market all the product categories together."""
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
    insight = """The highest total sales value is for "Books" followed by "Electronics".  \n"Books" is the top product these year, it have the highest number of selled quantities and the highest sales value and also the highest profit value"""
    st.markdown(insight)
    st.divider()


    # st.subheader("Total Profit Value for each category", width='content', divider='blue')
    # with col2:
    #     d = df.groupby('Category')['Profit'].sum().reset_index(name='Profit')
    #     fig = px.bar(
    #         d, 
    #         x='Category',
    #         y='Profit',
    #         # title='Total sal  es for each category',
    #         text_auto='.1f',
    #         color='Category'
    #     )
    #     st.plotly_chart(fig)
    # st.divider()



    # Region
    # d = df.groupby('Region')['Quantity'].sum().reset_index(name='Quantity')
    # fig = px.pie(d,
    #     names='Region',
    #     values='Quantity',
    #     title='Total Number of selled quantities in each Region',
    #     hole=0.3,
    #     )
    # st.plotly_chart(fig)
    # st.divider()
    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("Total Number of selled quantities in each Region", width='content', divider='blue')
        insight = """The highest Region sales is :green[South] followed by :green[North] by :green[~26\%] from totall number of selled products for each,
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

    # st.subheader("Total Profit Value for each region", width='content', divider='blue')
    # d = df.groupby('Region')['Profit'].sum().reset_index(name='Profit')
    # fig = px.bar(
    #     d, 
    #     x='Region',
    #     y='Profit',
    #     # title='Total profits for each Region',
    #     text_auto='.1f',
    #     color='Region'
    # )
    # st.plotly_chart(fig)
    # st.divider()
    # =======================================================================================================

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
    st.markdown(f"""The Average Net Profit is :green[{round((df['Profit'].sum()/df['Sales'].sum())*100,2)} %]""")
    st.divider()


    # st.subheader("Net Profit percentage for each region", width='content', divider='blue')
    # d = (df.assign(profit_percentage=(df['Profit']/df['Sales']*100))
    #     .groupby('Region')['profit_percentage']
    #     .mean() 
    #     .reset_index(name='profit_percentage')
    #     )
    # d['percent'] = d['profit_percentage'].apply(lambda x: f"{round(x, 2)} %")
    # fig = px.bar(
    #     d, 
    #     x='Region',
    #     y='profit_percentage',
    #     title='Net profit percentage for each region',
    #     text='percent',
    #     labels={'Region': 'Region', 'profit_percentage': 'Net Profit Percentage'},
    #     # text_auto='.1f',
    #     color='Region'
    # )
    # st.plotly_chart(fig)
    # st.divider()


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
    # st.subheader("""Total Sales over days""", width='content', divider='blue')
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
    # with col1:
        # st.subheader("""Total Sales over months for :blue[North] region only""", width='content', divider='blue')
        # North
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
    insight = """**At North Region**  \nThe highest pay rate category is :red[Clothing] with 13.4k at October, this is the start of the winter clothing"""
    st.markdown(insight)
    st.divider()
    # with col2:
        # south
        # st.subheader("""Total Sales over months for :blue[South] region only""", width='content', divider='blue')
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
        # st.divider()

    # with col1:
        # East
        # st.subheader("""Total Sales over months for :blue[East] region only""", width='content', divider='blue')
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
        # st.divider()
    # with col2:
        # West
        # st.subheader("""Total Sales over months for :blue[West] region only""", width='content', divider='blue')
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
    st.divider()


st.header("Complete Marketing Campaign", divider='blue')
st.subheader("1. For :blue[North] Region")
st.markdown("")

st.subheader("2. For :blue[South] Region")


st.subheader("3. For :blue[East] Region")


st.subheader("4. For :blue[West] Region")
