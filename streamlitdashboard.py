"""Authors:
    1) Raj Kumar Narendiran
    2) Pritesh Joshi
"""

import pandas as pd #pip install pandas openpyxl
import plotly.express as px #pip install streamlit
import streamlit as st #pip install plotly-express

print(pd. __version__)

file_path = "Sales.csv"
#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart",
    layout="wide"
)

customers = pd.read_csv(
    file_path
)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=customers["Country"].unique(),
    default=customers["Country"].unique()
)

gender = st.sidebar.multiselect(
    "Select the state:",
    options=customers["Customer_Gender"].unique(),
    default=customers["Customer_Gender"].unique()
)

age_group = st.sidebar.multiselect(
    "Select the Age_Group:",
    options=customers["Age_Group"].unique(),
    default=customers["Age_Group"].unique()
)

customers_selection = customers.query(
    "Country == @country & Customer_Gender == @gender & Age_Group == @age_group"
)

#st.dataframe(customers_selection)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(customers_selection["Revenue"].sum())
total_profit = int(customers_selection["Profit"].sum())


check_data_expander = st.expander("Check Data")
check_data_expander.write(customers_selection)
st.markdown("---")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with right_column:
    st.subheader("Total Profit:")
    st.subheader(f"US $ {total_profit:,}")

@st.cache
def convert_df(customers_selection):
    return customers_selection.to_csv().encode('utf-8')

sales_column, profit_column = st.columns(2)
#SALES BY PRODUCT [BAR CHART]
with sales_column:
    sales_by_product = (
        customers_selection.groupby(by=["Sub_Category"]).sum()[["Revenue"]].sort_values(by="Revenue")
    )

    fig_product_sales = px.bar(
        sales_by_product,
        x = "Revenue",
        y = sales_by_product.index,
        orientation="h",
        title="<b>Sales Revenue by Product </b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product),
        template="plotly_white"
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    fig_product_sales.update_layout(xaxis_title='Revenue', yaxis_title='Product')

    st.download_button(
        label="Download data as CSV",
        data=convert_df(sales_by_product),
        file_name='sales_by_product.csv',
        mime='text/csv',
    )

    # Displays the Left Bar Chart
    left_column.plotly_chart(fig_product_sales, use_container_width=True)
    check_data_expander = st.expander('Show in Table')
    check_data_expander.write(sales_by_product)

#PROFIT BY PRODUCT [BAR CHART]
with profit_column:
    profit_by_product = (
        customers_selection.groupby(by=["Sub_Category"]).sum()[["Profit"]].sort_values(by="Profit")
    )

    fig_product_profit = px.bar(
        profit_by_product,
        x = profit_by_product.index,
        y = "Profit",
        title="<b>Profit by Product </b>",
        color_discrete_sequence=["#0083B8"] * len(profit_by_product),
        template="plotly_white"
    )
    fig_product_profit.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    fig_product_profit.update_layout(xaxis_title='Product', yaxis_title='Profit')

    st.download_button(
        label="Download data as CSV",
        data=convert_df(profit_by_product),
        file_name='profit_by_product.csv',
        mime='text/csv',
    )

    # Displays the Right Bar Chart
    right_column.plotly_chart(fig_product_profit, use_container_width=True)
    check_data_expander = st.expander('Show in Table')
    check_data_expander.write(profit_by_product)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} 
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

yearwise, categorywise = st.columns(2)

# YearWise Profit, Revenue, Profit_Percentage Calculation
with yearwise:
    st.header("Year wise Sales")
    m_y_sales = customers_selection[["Year", "Profit", "Revenue"]].groupby(["Year"]).sum()
    m_y_sales["Profit_percentage"] = (m_y_sales["Profit"] / m_y_sales["Revenue"]) * 100
    st.bar_chart(m_y_sales)

    st.download_button(
        label="Download data as CSV",
        data=convert_df(m_y_sales),
        file_name='m_y_sales.csv',
        mime='text/csv',
    )

    check_data_expander = st.expander('Show in Table')
    check_data_expander.write(m_y_sales)

# CategoryWise Profit, Revenue, Profit_Percentage Calculation
with categorywise:
    st.header("category wise Sales")
    p_c_sales = customers_selection[["Product_Category", "Profit", "Revenue"]].groupby(["Product_Category"]).sum()
    p_c_sales["Profit_percentage"] = (p_c_sales["Profit"] / p_c_sales["Revenue"]) * 100
    st.bar_chart(p_c_sales)
    st.download_button(
        label="Download data as CSV",
        data=convert_df(p_c_sales),
        file_name='p_c_sales.csv',
        mime='text/csv',
    )
    check_data_expander = st.expander('Show in Table')
    check_data_expander.write(p_c_sales)
