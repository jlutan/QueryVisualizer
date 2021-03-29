import streamlit as st
import pandas as pd
import flat_table
import networkx as nx
import pandas.plotting._matplotlib

def main(graph, authToken):
    """ 
    Prompts the user for which task to perform and calls the corresponding function 

    :param graph: instance of TigerGraphConnection
    :type graph: TigerGraphConnection
    :param authToken: authorization token to access graph
    :type authToken: tuple
    """
    
    task = st.selectbox("Task Select", ["Run an Installed Query", "Write a Custom Query"])
    if task == "Run an Installed Query":
        installedQuery(graph)
            
    elif task == "Write a Custom Query":
        customQuery(graph)



def installedQuery(graph):
    """ 
    Prompts the user to choose an installed query, define its arguments, and choose the display format 
    
    :param graph: instance of TigerGraphConnection
    :type graph: TigerGraphConnection
    """
    
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
    data_format = st.selectbox("Output Format", ["JSON", "Table"])
    if st.button("Run Query"):
        query = graph.runInstalledQuery(command[17:], args) # returns JSON object
        if data_format == "JSON":
            st.json(query)
        elif data_format == "Table":
            df = pd.DataFrame(query[0][list(query[0].keys())[0]])
            data = flat_table.normalize(df)
            st.table(data)
        # elif data_format == "Graph":
        #     df = pd.DataFrame(query[0][list(query[0].keys())[0]], columns=[ i for i in range(0, len(query[0][list(query[0].keys())[0]]))])
        #     G = nx.from_pandas_adjacency(df)
        #     st.write(G)
        # elif data_format == "Chart":
        #     chart_format = st.selectbox("Chart Type", ["Line Chart", "Area Chart", "Bar Chart", "Altair"])
            
        #     if st.checkbox("Run Query"):
        #         query = graph.runInstalledQuery(command[17:], args) # run query on db
        #         st.write(query)
        #         x = st.selectbox("x-axis", labels)
        #         y = st.selectbox("y-axis", labels)
        #         df = pd.DataFrame(query[0])
        #         if st.button("Display Output"):
        #             if chart_format == "Line Chart":
        #                 st.line_chart(df)
        #             elif chart_format == "Area Chart":
        #                 st.area_chart(df)
        #             elif chart_format == "Bar Chart":
        #                 st.bar_chart(df)
        #             elif chart_format == "Altair":
        #                 pass



def customQuery(graph):
    """ 
    Prompts the user to write a custom query, define its arguments, and choose the display format 

    :param graph: instance of TigerGraphConnection
    :type graph: TigerGraphConnection
    """
    
    st.header("Write a Custom Query")
    st.write("Write an interpreted GSQL query to the database, define arguments, and choose how ot display the output.")
    st.markdown("**Note: Start the query with 'INTERPRET QUERY () FOR GRAPH $graphname { }**")
    custom = st.text_area("Write a Query", 
    '''INTERPRET QUERY (STRING str, INT num) FOR GRAPH $graphname {
        PRINT str;
        PRINT num;
    }
    '''
    , height=250)
    args = st.text_input("Enter list of arguments separated with '&'", "str=nothing&num=25")
    
    st.header("Output")
    data_format = st.selectbox("Output Format", ["JSON", "Table"])
    if st.button("Run Query"):
        query = query = graph.runInterpretedQuery(custom, args) # returns JSON object
        if data_format == "JSON":
            st.json(query)
        elif data_format == "Table":
            df = pd.DataFrame(query[0], index=[x for x in range(0, len(query[0]))])
            data = flat_table.normalize(df)
            st.table(data)