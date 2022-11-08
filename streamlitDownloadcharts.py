import streamlit as st
import pandas as pd

file_path = "Sales.csv"

st.set_page_config(
    page_title="Bike Sales Analytics",
    layout="wide"
)
df = pd.read_csv(file_path)

st.title("Bike Sales Analytics")

check_data_expander = st.expander("Check Data")
check_data_expander.write(df)

col1, col2 = st.columns(2)

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

with col1:
    st.header("Year wise Sales")
    m_y_sales = df[["Year", "Profit", "Revenue"]].groupby(["Year"]).sum()
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


with col2:
    st.header("category wise Sales")
    p_c_sales = df[["Product_Category", "Profit", "Revenue"]].groupby(["Product_Category"]).sum()
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




with st.sidebar:

    options = st.multiselect(
        'Select Columns to Download CSV',
        df.columns.values
        )
    selected_df = df[options]
    csv = convert_df(selected_df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
