import pyTigerGraphBeta as tg
import streamlit as st

import tasks

def main():
    """ 
    Gets login credentials from the user and
    establishes a connection to the TigerGraph database 
    """
    
    st.title("TigerGraph Visual Query Tool")

    st.write("Welcome to my first Streamlit + TigerGraph project connecting a web application to a graph database and visualizing query data.")

    graph = None
    authToken = None

    sb = st.sidebar
    sb.header("Connect to TigerGraph Database")
    host = sb.text_input("Host URL")
    username = sb.text_input("Username")
    password = sb.text_input("Password", type="password")
    graphname = sb.text_input("Graph Name")
    if sb.checkbox("Connect to Graph"):
        # establish connection to TG database
        graph = tg.TigerGraphConnection(
            host=host, 
            username=username, 
            password=password, 
            graphname=graphname, 
        )
        st.success(f"Connected to {graphname} graph")
        secret = sb.text_input("Secret", type="password")
        if (sb.checkbox("Get Auth Token")):
            # get auth token using user inputted secret
            authToken = graph.getToken(secret)
            tasks.main(graph, authToken)