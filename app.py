# -----Import modules-------
import pickle
from pathlib import Path
import yaml

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
from yaml import SafeLoader

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",  # Reference emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

# ----- USER AUTHENTIUCATION -----
with open('config_hashpassw.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    # ------READ EXCEL FILE------
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000
    )
    # Add 'hour' column to the dataframe:
    df['hour'] = pd.to_datetime(df.Time, format="%H:%M:%S").dt.hour

    # -----Sidebar-----
    st.sidebar.title(f"Welcome {name}!")
    authenticator.logout("Logout", "sidebar")

    st.sidebar.header("Please filter here: ")
    city = st.sidebar.multiselect(
        "Select the City: ",
        options=df['City'].unique(),
        default=df['City'].unique()
    )

    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique(),
    )

    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    payment = st.sidebar.multiselect(
        "Select the Payment method:",
        options=df["Payment"].unique(),
        default=df["Payment"].unique()
    )

    df_selection = df.query(
        'City == @city & Customer_type == @customer_type & Gender == @gender & Payment == @payment'
    )

    # print the dataframe to streamlit app:
    st.dataframe(df_selection)

    # ---- MAINPAGE ----
    st.title(":bar_chart: Sales Dashboard")
    st.markdown("##")  # To separate the title from KPI's

    # ------- KPI's ------
    total_sales = int(df_selection['Total'].sum())
    avg_rating = round(df_selection['Rating'].mean(), 1)
    star_rating = ":star:" * int(round(avg_rating, 0))
    avg_sale_by_transaction = round(df_selection['Total'].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)  # Splitting into 3 columns for visualization:
    with left_column:
        st.subheader("Total Sales: ")
        st.subheader("US $ {}".format(total_sales))
    with middle_column:
        st.subheader("Average Rating: ")
        st.subheader(f"{avg_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sale/ Transaction: ")
        st.subheader(f"US $ {avg_sale_by_transaction}")

    st.markdown("""---""")

    # -------- BAR CHART: (Sales by Product Line) ------
    sales_by_product_line = (
            df_selection.groupby(by=["Product line"]).sum()[['Total']].sort_values(by="Total")
    )
    # Using plotly to plot the bar chart:
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="Sales by Product Line",
        color_discrete_sequence=['#0083B8']*len(sales_by_product_line),
        template="plotly_white"
    )
    # Removing the background of the barchart (to give a transparent look):
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # -------- BAR CHART: (Sales by Hours) ------
    sales_by_hour = (
            df_selection.groupby(by=["hour"]).sum()[['Total']].sort_values(by="Total")
    )
    # Using plotly to plot the bar chart:
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        orientation="v",
        title="Sales by Hour",
        color_discrete_sequence=['#0083B8']*len(sales_by_hour),
        template="plotly_white"
    )
    # Removing the background of the barchart (to give a transparent look):
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    # To plot both the charts side by side:
    left_col, right_col = st.columns(2)
    left_col.plotly_chart(fig_product_sales, use_container_width=True)
    right_col.plotly_chart(fig_hourly_sales, use_container_width=True)

    # ------ Hide streamlit Styles -----------
        # Removes Main menu on top right hand side,
        # Removes footer ('Made with Streamlit')
        # Removes header (color line at the top)
    hide_st_style = """
                <style>
                #Mainmenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>
                    """

    st.markdown(hide_st_style, unsafe_allow_html=True)