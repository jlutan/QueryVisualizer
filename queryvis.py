import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os import getenv
import flat_table

load_dotenv()

def main():
    sb = st.sidebar

    TG_HOST = getenv('HOST')
    TG_GRAPHNAME = getenv('GRAPHNAME')
    TG_USERNAME = getenv('USERNAME')
    TG_PASSWORD = getenv('PASSWORD')
    TG_SECRET = getenv('SECRET')


    st.title("TigerGraph Visual Query Tool")

    st.write("Welcome to my first Streamlit + TigerGraph project connecting a web application to a graph database and visualizing query data.")

    graph = None
    authToken = None

    sb.header("Connect to TigerGraph Database")
    host = sb.text_input("Host URL") or TG_HOST
    username = sb.text_input("Username") or TG_USERNAME
    password = sb.text_input("Password", type="password") or TG_PASSWORD
    graphname = sb.text_input("Graph Name") or TG_GRAPHNAME
    if sb.checkbox("Connect to Graph"):
        # establish connection to TG database
        graph = tg.TigerGraphConnection(
            host=host, 
            username=username, 
            password=password, 
            graphname=graphname, 
        )
        st.success("Connected to {} graph".format(graphname))
        secret = sb.text_input("Secret", type="password")
        if (sb.checkbox("Confirm Secret")):
            authToken = graph.getToken(secret or TG_SECRET)
            app(graph, authToken)

        
def app(graph, authToken):
    query = None
    custom = None
    params = None
    df = None
    data = None

    task = st.selectbox("Task Select", ["Run an Installed Query", "Write a Custom Query"])
    if task == "Run an Installed Query":
        st.header("Run an Installed Query")
        st.write("Run any queries currently installed on the graph database. Pick a query, define arguments on-the-fly, and choose how to display the output.")
        
        # st.subheader("Currently Installed Queries")
        # st.json(graph.getInstalledQueries())
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
                params[p] = st.number_input(p + ": " + ptype, min_value= int(-(1<<53)+1), max_value=int((1<<53)-1), value=0, step=1, key=i)
            elif (ptype == "STRING"):
                params[p] = st.text_input(p + ": " + ptype, value="blank", key=i)
            
    elif task == "Write a Custom Query":
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
            if task == "Run an Installed Query":
                query = graph.runInstalledQuery(choice[17:], params) # run query on db
                df = pd.DataFrame(query[0])
            elif task == "Write a Custom Query":
                query = graph.runInterpretedQuery(custom, params) # run custom query on db
                df = pd.DataFrame(query[0], [x for x in range(0, len(query[0]))])
            # df.dropna(subset=)
            data = flat_table.normalize(df)
            st.table(data)
    elif data_format == "Chart":
        chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
        if st.button("Run Query"):
            if task == "Run an Installed Query":
                query = graph.runInstalledQuery(choice[17:], params) # run query on db
                df = pd.DataFrame(query[0])
            elif task == "Write a Custom Query":
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



if __name__ == "__main__":
    main()