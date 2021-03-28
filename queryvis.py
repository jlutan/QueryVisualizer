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

st.title("TigerGraph Visual Query Tool")

st.write("Welcome to my first TigerGraph + Streamlit project connecting a web application to a graph database and visualizing query data.")

sb = st.sidebar
selection = sb.selectbox("Function Select", ["Run an Installed Query", "Write a Custom Query"])

query = None
custom = None
params = None
df = None
data = None

if selection == "Run an Installed Query":
    st.header("Run an Installed Query")
    st.write("Run any queries currently installed on the graph database. Pick a query, define arguments on-the-fly, and choose how to display the output.")
    
    st.subheader("Currently Installed Queries")
    st.json(graph.getInstalledQueries())
    installed = graph.getInstalledQueries()
    names = installed.keys()
    
    st.subheader("Choose an Installed Query")
    choice = st.selectbox("Query", list(names))
    
    # get arguments from user
    st.subheader("Define arguments")
    temp = installed[choice]["parameters"].keys()
    temp = list(filter(lambda p : p != "query", temp))
    params = { key : None for key in temp }
    for i in range(0, len(temp)):
        p = temp[i]
        ptype = installed[choice]["parameters"][p]["type"]
        if (ptype == "INT64"):
            params[p] = st.number_input(p + ": " + ptype, min_value= -1000, max_value=1000, value=0, step=1, key=i)
        elif (ptype == "STRING"):
            params[p] = st.text_input(p + ": " + ptype, value="blank", key=i)
        
elif selection == "Write a Custom Query":
    st.header("Write a Custom Query")
    st.write("Write an interpreted GSQL query to the database, define arguments, and choose how ot display the output.")
    st.markdown("**Note: Start the query with 'INTERPRET QUERY () FOR GRAPH $graphname { }**")
    custom = st.text_area("Write a Query", 
    '''INTERPRET QUERY (STRING str) FOR GRAPH $graphname {
        PRINT str;
    }
    '''
    , height=250)
    params = st.text_input("Enter list of arguments separated with '&'", "str=nothing")
    

st.header("Output")
data_format = st.selectbox("Output Format", ["Table", "Chart", "Map"])
if data_format == "Table":
    if st.button("Run Query"):
        if selection == "Run an Installed Query":
            query = graph.runInstalledQuery(choice[17:], params) # run query on db
            df = pd.DataFrame(query[0], [x for x in range(0, len(query[0]))])
        elif selection == "Write a Custom Query":
            query = graph.runInterpretedQuery(custom, params) # run custom query on db
            df = pd.DataFrame(query[0], [x for x in range(0, len(query[0]))])
        data = flat_table.normalize(df)
        st.table(data)
elif data_format == "Chart":
    chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
    if st.button("Run Query"):
        if selection == "Run an Installed Query":
            query = graph.runInstalledQuery(choice[17:], params) # run query on db
            df = pd.DataFrame(query[0])
        elif selection == "Write a Custom Query":
            query = graph.runInterpretedQuery(custom, params)
            df = pd.DataFrame(query[0])
        if chart_format == "Line Chart":
            st.line_chart(df)
        elif chart_format == "Area Chart":
            st.area_chart(df)
        elif chart_format == "Bar Chart":
            st.bar_chart(df)
# elif data_format == "Map": # WIP
#     data = df
#     st.map(data)