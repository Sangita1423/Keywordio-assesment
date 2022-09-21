from sqlite3 import InterfaceError
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
 
    server = '10.1.1.142'
    database = 'UNOFINANCE_REPORT' 
    username = 'uno' 
    password = 'devmis123'  
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    # select 26 rows from SQL table to insert in dataframe.
    query = "SELECT * FROM ExpDumpAsonDate_Final_test"
    df = pd.read_sql(query, cnxn)
    #print(df.head(26))


    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["VoucherDt"], format="%H:%M:%S").dt.hour
    #return df
    df["JMDGRPUNIT"] = df["JMDGRPUNIT"] 
    return df

data = get_data_from_excel()
data = data.rename(columns={"JMDGRPUNIT": "jmdgrpunit", "ZONEGRPUNIT": "zonegrpunit" })

ics = data['jmdgrpunit'].drop_duplicates()
ics_choice = st.sidebar.selectbox("Select your jmdgrpunit:", ics)
practices = list(data["zonegrpunit"].loc[data["jmdgrpunit"] == ics_choice].drop_duplicates())
practice_choice = st.sidebar.multiselect("Select zonegrpunit", practices)
#practices1 = list(data["unitshrtdescr"].loc[data["zonegrpunit"] == practice_choice])
#practice_choice1 = st.sidebar.multiselect("Select unitshrtdescr", practices1)
data1 = data.loc[(data['jmdgrpunit'] == ics_choice) & (data['zonegrpunit'].isin(practice_choice)) ] 
#data2 = data.loc[(data['zonegrpunit'] == practice_choice) & (data['unitshrtdescr'].isin(practice_choice1)) ] 
#new_dataframe = pd.concat([data1,data2]).drop_duplicates()

data2 = get_data_from_excel()
data2 = data2.rename(columns={"ZONEGRPUNIT": "zonegrpunit", "UnitShrtDescr": "unitshrtdescr"})
#
#ics2 = data2['zonegrpunit'].drop_duplicates()
#ics_choice2 = st.sidebar.selectbox("Select your zonegrpunit:", ics2)
practices2 = list(data2["unitshrtdescr"].loc[data2["zonegrpunit"] == practice_choice].drop_duplicates())
practice_choice2 = st.sidebar.multiselect("Select unitshrtdescr", practices2)
##practices1 = list(data["unitshrtdescr"].loc[data["zonegrpunit"] == practice_choice])
##practice_choice1 = st.sidebar.multiselect("Select unitshrtdescr", practices1)
data3 = data2.loc[(data1['zonegrpunit'] == practice_choice) & (data2['unitshrtdescr'].isin(practice_choice2)) ] 
#data2 = data.loc[(data['zonegrpunit'] == practice_choice) & (data['unitshrtdescr'].isin(practice_choice1)) ] 
#new_dataframe = pd.concat([data1,data2]).drop_duplicates()
# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(data["Amount"].sum())
average_rating = round(data["Rating"].mean(), 1)
star_rating = ":star:" #* int(round(average_rating, 0))
average_sale_by_transaction = round(data["Amount"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Amount:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    data1.groupby(by=["zonegrpunit"]).sum()[["Amount"]].sort_values(by="Amount")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="Amount",
    #orientation="v",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    yaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = data1.groupby(by=["zonegrpunit"]).sum()[["Amount"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Amount",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
