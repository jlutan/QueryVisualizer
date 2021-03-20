import pyTigerGraphBeta as tg
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os import getenv

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

st.header("Currently Installed Queries:")
if st.checkbox("Show queries:"):
    st.write(graph.getInstalledQueries())

st.header("Query Example:")


query = graph.runInstalledQuery("topSideEffectsForTopDrugs")
# params="companyName=PFIZER&k=5&role=PS")


# query = graph.runInterpretedQuery(
#     """
#     INTERPRET QUERY (STRING companyName, INT k, STRING role) FOR GRAPH faers {
#         # Define a heap structure which sorts the reaction map (below) by count
#         TYPEDEF TUPLE<STRING name, INT cnt> tally;
#         HeapAccum<tally>(k, cnt DESC) @topReactions;
            
#         # Keep count of how many times each reaction or drug is mentioned.
#         ListAccum<STRING> @reactionList;
#         SumAccum<INT> @numCases;
#         MapAccum<STRING, INT> @reactionTally;

#     # 1. Find all the cases where the given pharma company is the 'mfr_sndr'
#     Company ={PharmaCompany.*};
#     Cases = SELECT c
#         FROM Company:s -(relatedTo:e)-> ReportedCase:c
#         WHERE s.mfr_sndr == companyName
#         ;

#         # 2. For each case, attach a list of its reactions
#         Tally = SELECT r
#         FROM Cases:c -(hasReactions:e)-> Reaction:r
#         ACCUM c.@reactionList += r.pt;
            
#         # 3. Find all the drug sequences for the selected cases, and transfer
#         #    the reaction list to the drug sequence.
#         DrugSeqs = SELECT ds
#         FROM Cases:c -(hasSequences:e)-> DrugSequence:ds
#         WHERE (role == "" OR ds.role_cod == role)
#             ACCUM ds.@reactionList = c.@reactionList
#     ;
        
#         # 4. Count the occurences of each drug mentioned in each drug sequence.
#         #    Also count the occurences of each reaction.
#         TopDrugs = SELECT d
#         FROM DrugSeqs:ds -(hasDrugs:e)-> Drug:d
#         ACCUM d.@numCases += 1,
#         FOREACH reaction in ds.@reactionList DO
#                 d.@reactionTally += (reaction -> 1)
#             END
#         ORDER BY d.@numCases DESC
#         LIMIT k
#         ;
            
#         # 5. Find only the Top K side effects for each selected Drug
#         TopDrugs = SELECT d
#             FROM TopDrugs:d 
#             ACCUM
#             FOREACH (reaction, cnt) IN d.@reactionTally DO
#                 d.@topReactions += tally(reaction,cnt)
#             END
#             ORDER BY d.@numCases DESC
#             ;
        
#         PRINT TopDrugs[TopDrugs.prod_ai, TopDrugs.@numCases, TopDrugs.@topReactions];
#     }
#     """,
#     params={
#         "companyName": "PFIZER",
#         "k": 5,
#         "role": "PS"
#     }
# )

df = pd.DataFrame(query[0]["TopDrugs"])

st.table(df)