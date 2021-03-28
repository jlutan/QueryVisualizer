import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd
import flat_table

def main(graph, authToken):
    """ Determines which task to perform and calls the corresponding function """
    
    task = st.selectbox("Task Select", ["Run an Installed Query", "Write a Custom Query"])
    if task == "Run an Installed Query":
        installedQuery(graph)
            
    elif task == "Write a Custom Query":
        customQuery(graph)



def installedQuery(graph):
    """ Prompts the user to choose an installed query,
    define its arguments, and choose the display format """
    
    st.header("Run an Installed Query")
    st.write("Run any queries currently installed on the graph database. Pick a query, define arguments on-the-fly, and choose how to display the output.")
    
    # st.subheader("Currently Installed Queries")
    # st.json(graph.getInstalledQueries())
    installed = graph.getInstalledQueries()
    names = installed.keys()
    
    st.subheader("Choose an Installed Query")
    command = st.selectbox("Query", list(names))
    
    # get arguments from user
    st.subheader("Define arguments")
    temp = installed[command]["parameters"].keys()
    temp = list(filter(lambda p : p != "query", temp))
    args = { key : None for key in temp }
    for i in range(0, len(temp)):
        p = temp[i]
        ptype = installed[command]["parameters"][p]["type"]
        if (ptype == "INT64"):
            args[p] = st.number_input(f"{p}: {ptype}", min_value= int(-(1<<53)+1), max_value=int((1<<53)-1), value=0, step=1, key=i)
        elif (ptype == "STRING"):
            args[p] = st.text_input(f"{p}: {ptype}", value="blank", key=i)
    
    st.header("Output")
    data_format = st.selectbox("Output Format", ["Table", "Chart", "Map"])
    if data_format == "Table":
        if st.button("Run Query"):
            query = graph.runInstalledQuery(command[17:], args) # run query on db
            df = pd.DataFrame(query[0])
            st.write(query)
            # df.dropna(subset=)
            data = flat_table.normalize(df)
            st.table(df)
    elif data_format == "Chart":
        chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
        if st.button("Run Query"):
            query = graph.runInstalledQuery(command[17:], args) # run query on db
            df = pd.DataFrame(query[0])
        if chart_format == "Line Chart":
            st.line_chart(df)
        elif chart_format == "Area Chart":
            st.area_chart(df)
        elif chart_format == "Bar Chart":
            st.bar_chart(df)



def customQuery(graph):
    """ Prompts the user to write a custom query,
    define its arguments, and choose the display format """
    
    st.header("Write a Custom Query")
    st.write("Write an interpreted GSQL query to the database, define arguments, and choose how ot display the output.")
    st.markdown("**Note: Start the query with 'INTERPRET QUERY () FOR GRAPH $graphname { }**")
    custom = st.text_area("Write a Query", 
    '''INTERPRET QUERY (STRING str) FOR GRAPH $graphname {
        PRINT str;
    }
    '''
    , height=250)
    args = st.text_input("Enter list of arguments separated with '&'", "str=nothing")
    
    st.header("Output")
    data_format = st.selectbox("Output Format", ["Table", "Chart", "Map"])
    if data_format == "Table":
        if st.button("Run Query"):
            query = graph.runInterpretedQuery(custom, args) # run custom query on db
            df = pd.DataFrame(query[0], [x for x in range(0, len(query[0]))])
            # df.dropna(subset=)
            data = flat_table.normalize(df)
            st.table(data)
    elif data_format == "Chart":
        chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart"])
        if st.button("Run Query"):
            query = graph.runInterpretedQuery(custom, args)
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