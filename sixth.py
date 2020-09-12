import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import SessionState
import base64
import helpers as hel

st.set_option('deprecation.showfileUploaderEncoding', False)

data = [["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"]]
# , tablout = pd.DataFrame(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"], columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])

# Sidebar
st.sidebar.subheader("Steward")
stewardlist = ["ADSantos", "ASRicamara", "KManingat", "LPalabay", "MAlvarado", "MMarcos", "RVillareal"]
stewardName = st.sidebar.selectbox(
    'Select steward username',
     stewardlist)
approval = ""

# getCSV
st.sidebar.subheader("Upload CSV File")
file_CSV = st.sidebar.file_uploader("Drag file here or click browse files", type=["csv"])
remark = st.sidebar.text_input("Remarks")
if st.sidebar.button("Approve"):
    approval = "APPROVED"
else:
    pass
if st.sidebar.button("Reject"):
    approval = "REJECTED"
else:
    pass

# Sidebar end
        
# Variables
table_prepped = hel.prep_csv(file_CSV)
state = SessionState.get(j = 0, t = 0,ta = 0, k = 0, r = 0, tablout = pd.DataFrame(), taken = 0)
    
matches = hel.count_matches(table_prepped.loc[table_prepped["PIVOT"].isnull()])
st.sidebar.write(state.r, " out of ", matches)
totalrows = len(table_prepped.index)

table_pivots = table_prepped.loc[(table_prepped['PIVOT'] == "PIVOT") | (table_prepped['PIVOT'] == "SIBLING")] 
pivots = hel.count_clusters(table_prepped)
totalpivots = len(table_pivots.index)
totalmatch = matches + totalpivots
totalclusters = pivots

# FUNCTIONS

def writePivot(pivot, steward):
    pivot.STEWARD = steward
    pivot.DATE_APPROVED = datetime.now()
    pivot.STEWARD_APPROVAL = "PIVOT"
    state.tablout = state.tablout.append(pivot, ignore_index=True)

def modRow(record, approval, taken, steward):
    record.STEWARD = steward
    record.DATE_APPROVED = datetime.now()
    record.STEWARD_APPROVAL = approval
    record.TIME_TAKEN = taken
    state.tablout = state.tablout.append(record, ignore_index = True)


def tableReports(rows, clusters, pivots, matches):
    taken = state.tablout['TIME_TAKEN'].sum()
    data = [[rows, clusters, pivots, matches, taken]]
    report = pd.DataFrame(data, columns=["ROWS", "CLUSTERS", "PIVOTS", "MATCHES", "TIME_TAKEN"])
    return report

def tableCluster(clusterid, tablout):
    return tablout.loc[(tablout["CLUSTER_ID"] == clusterid)]

table_new = pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
def tablePivots(table_pivots, steward):    
    i = 0
    for index, row in table_pivots.iterrows():
        row.STEWARD_APPROVAL = "PIVOT"
        row.STEWARD = steward
        row.DATE_APPROVED = datetime.now()
        row.TIME_TAKEN = 0
        table_new.loc[i] = row
        i+=1
    else:
        return table_new


def tableMatches(matchid, table_prepped):
    table_matches = table_prepped.loc[(table_prepped["MATCH_ID"] == matchid) & (table_prepped["PIVOT"] != "PIVOT") & (table_prepped["PIVOT"] != "SIBLING")]
    table_matches_prepped =  pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
    
    for index, row in table_matches.iterrows():
        table_matches_prepped.loc[index] = row
        
    else:
        pass
    #prepmatches.count = count_matches(table_matches_prepped)
    return table_matches_prepped


# DISPLAY WELCOME
st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'
st.write("TABLOUT")
st.write(state.tablout)

while state.j < pivots:
    pivot = tablePivots(table_pivots, stewardName).loc[state.j]
    matchid = pivot['MATCH_ID']
    table_matches = tableMatches(matchid, table_prepped)
    matchto = hel.count_matches(table_matches)
    st.write('MATCH_ID: ', matchid, "    Match Count: ", matchto)
    proceed = ""
    while state.k < matchto:
        match = table_matches.loc[state.k]
        outable = pd.concat([pivot, match], axis = 1)
       
        st.write("stuff")
        if approval == "":
            st.write(outable)
            st.write( state.t)
            while approval == "":
                time.sleep(.5)
                state.taken += 1
                st.text(state.taken)
            else:
                time.sleep(5)
                st.write("HALAAA")
                
        else:
            modRow(match, approval, state.taken, stewardName)
            state.taken = 0
            approval = ""
            state.k += 1
            state.r += 1
            
    else:
       
        if proceed == "":
            if st.button("Next"):
                proceed = "Next"
            else:
                pass
            clusterid = pivot.CLUSTER_ID
            writePivot(pivot, stewardName)
            st.write("tablout")
            st.write(state.tablout)
            st.write("cluster")
            st.write(tableCluster(clusterid, state.tablout))
            while proceed == "":
                time.sleep(0.5)
                st.write('sleeping')
            else:
                state.j += 1
                state.k = 0
                #remove these
                proceed = ""
                st.write(state.j)
                st.write(state.t)
                
        else: 
            pass             
                 
else:
    st.write("All matches complete!")
    st.write(tableReports(state.tablout, totalrows, totalclusters, totalpivots, totalmatch))
    st.markdown(hel.get_download(state.tablout), unsafe_allow_html=True)
    #PRINT OUT report data
