import pandas as pd #pip install pandas openpyxl
import plotly.express as px #pip install streamlit
import streamlit as st #pip install plotly-express

print(pd. __version__)

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart",
    layout="wide"
)

customers = pd.read_csv(
    'Sales.csv'
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

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with right_column:
    st.subheader("Total Profit:")
    st.subheader(f"US $ {total_profit:,}")

st.markdown("---")
st.dataframe(customers_selection)

#SALES BY PRODUCT [BAR CHART]
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
fig_product_sales .update_layout(xaxis_title='Revenue', yaxis_title='Product')

#PROFIT BY PRODUCT [BAR CHART]
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

fig_product_profit .update_layout(xaxis_title='Product', yaxis_title='Profit')

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_product_profit, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} 
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

