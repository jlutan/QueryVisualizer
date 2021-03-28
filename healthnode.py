import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os import getenv
import flat_table

load_dotenv()
TG_HOST = "https://healthnode.i.tgcloud.io"
TG_GRAPHNAME = "faers"
TG_USERNAME = "tigergraph"
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

df = None
data = None

if selection == "Run an Installed Query":
    st.header("Run an Installed Query")
    st.write("Run any queries currently installed on the graph database. Pick a query, define arguments on-the-fly, and choose how to display the output.")
    
    st.subheader("Currently Installed Queries")
    queries = list(map(lambda q : q["parameters"]["query"]["default"], graph.getInstalledQueries().values()))
    
    installed = st.selectbox("Currently Installed Queries", queries)
    params = st.text_input("Enter parameters separated with '&'", "companyName=PFIZER")
    query = graph.runInstalledQuery(installed, params)
    df = pd.DataFrame(query[0])
    # st.header("Query Example")

    # # run installed query
    # query = graph.runInstalledQuery("mostReportedDrugsForCompany_v2", params="companyName=PFIZER&k=5&role=PS")

    # # convert raw query to pandas Data Frame
    # df = pd.DataFrame(query[0]["TopDrugs"])

elif selection == "Write a Custom Query":
    st.header("Write a Custom Query")
    st.write("Write an interpreted GSQL query to the database, define arguments, and choose how ot display the output.")
    user_input = st.text_area("Write a Query", 
    '''INTERPRET QUERY (STRING companyName) FOR GRAPH $graphname { // NOTE: DO NOT REMOVE THIS LINE
        PRINT companyName;
    }
    ''',
    height=250)
    params = st.text_input("Enter parameters separated with '&'", "companyName=PFIZER")
    query = graph.runInterpretedQuery(user_input, params)
    df = pd.DataFrame(query[0], [x for x in range(0, len(query[0]))])

st.header("Output")
data_format = st.selectbox("Output Format", ["Table", "Chart", "Map"])
if data_format == "Table":
    data = flat_table.normalize(df)
    st.table(data)
elif data_format == "Chart":
    chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
    data = df
    if chart_format == "Line Chart":
        st.line_chart(data)
    elif chart_format == "Area Chart":
        st.area_chart(data)
    elif chart_format == "Bar Chart":
        st.bar_chart(data)
# elif data_format == "Map": # WIP
#     data = df
#     st.map(data)