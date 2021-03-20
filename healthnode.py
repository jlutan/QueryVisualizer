import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os import getenv
import flat_table

load_dotenv()
TG_HOST = "https://healthnode.i.tgcloud.io"
TG_GRAPHNAME = "faers"
TG_USERNAME = getenv('USERNAME')
TG_PASSWORD = getenv('PASSWORD')
TG_SECRET = getenv('SECRET')

# establish connection to TG database
graph = tg.TigerGraphConnection(
    host=TG_HOST, 
    username=TG_USERNAME, 
    password=TG_PASSWORD, 
    graphname=TG_GRAPHNAME, 
)

authToken = graph.getToken(TG_SECRET)
# print(authToken)

# results = graph.getEndpoints()
# print(results)

st.title("HealthNode Graph")

st.write("Welcome to my first TigerGraph and Streamlit project connecting a web application to a graph database and visualizing query data.")

sb = st.sidebar
selection = sb.selectbox("Function Select", ["Run an Installed Query", "Write a Custom Query"])

data = pass

if selection == "Run an Installed Query":
    st.header("Run an Installed Query")
    st.write("This interface will allow you to run any queries currently installed in the cloud database. Pick a query, specify arguments on-the-fly, and view the output as a table, chart, or map.")
    
    st.subheader("Currently Installed Queries")
    if st.checkbox("Show queries"):
        df = pd.DataFrame(graph.getInstalledQueries())
        data = flat_table.normalize(df)
        st.table(data)
    
    st.header("Query Example")

    # run installed query
    query = graph.runInstalledQuery("topSideEffectsForTopDrugs", params="companyName=PFIZER&k=5&role=PS")

    # convert raw query to pandas Data Frame
    df = pd.DataFrame(query[0]["TopDrugs"])
    data = flat_table.normalize(df)

    # print to streamlit app
    st.table(data)
elif selection == "Write a Custom Query":
    pass

st.header("Output")
data_format = st.selectbox("Output Format", ["Table", "Chart", "Map"])
if data_format == "Table":
    st.table(data)
elif data_format == "Chart":
    chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
    if chart_format == "Line Chart":
        st.line_chart()
    elif chart_format == "Area Chart":
        pass
    elif chart_format == "Bar Chart":
        pass 
elif data_format == "Map":
    pass