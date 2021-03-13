import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd

TG_HOST = "https://healthnode.i.tgcloud.io"
TG_GRAPHNAME = "HealthNode"
TG_USERNAME = "tigergraph"
TG_PASSWORD = "rainbow456"
TG_SECRET = "8j7iqhlf83tcpoq0sef1i0tkf7fcm6kr"

# conn = tg.TigerGraphConnection(host=TG_HOST, graphname=TG_GRAPHNAME, username=TG_USERNAME, password=TG_PASSWORD)

st.title("HealthNode Graph")
st.markdown("Welcome to my first TigerGraph and Streamlit project visualizing sample medical data in a web application environment.")
st.header("Graph")
