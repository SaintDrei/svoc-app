import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time
import threading
import SessionState
import base64

st.set_option('deprecation.showfileUploaderEncoding', False)

data = [["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "REMARKS", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"]]
# , tablout = pd.DataFrame(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"], columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])

# Sidebar
st.sidebar.subheader("Steward")
stewardlist = ["ADSantos", "ASRicamara", "KManingat", "LPalabay", "MAlvarado", "MMarcos", "RVillareal"]
stewardName = st.sidebar.selectbox(
    'Select steward username',
     stewardlist)
approval = ""
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

#Functions
st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'
def prep_csv():
    try:
        table_CSV = pd.read_csv(file_CSV)        
        return table_CSV
    except:
        return st.markdown("<font color='red'><strong>Please upload CSV on the sidebar</strong></font>", unsafe_allow_html=True)
        

def count_clusters(x):
    counts = x["STEWARD_APPROVAL"].value_counts()
    y = counts.iloc[0]
    return y

def count_matches(x):
    y = x["MATCH_ID"].value_counts()
    return y.sum(axis=0)



        
# Variables

table_prepped = prep_csv()
state = SessionState.get(j = 0, t = 0,ta = 0, k = 0, r = 0, tablout = pd.DataFrame(), taken = 0)
    
def writeRow(row, approval, prev, table_OUT):   
    towrite =  table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID]
    towrite.STEWARD_APPROVAL = approval
    towrite.DATE_APPROVED = datetime.now()
    towrite.STEWARD = stewardName
    towrite.TIME_TAKEN = datetime.now() - prev
    st.write(towrite)

def writePivot(pivot):
    pivot.STEWARD = stewardName
    pivot.DATE_APPROVED = datetime.now()
    pivot.STEWARD_APPROVAL = "PIVOT"
    state.tablout = state.tablout.append(pivot, ignore_index=True)


def modRow(record, approval, taken, remarks):
    record.STEWARD = stewardName
    record.DATE_APPROVED = datetime.now()
    record.STEWARD_APPROVAL = approval
    record.TIME_TAKEN = taken
    record.REMARKS = remarks
    state.tablout = state.tablout.append(record, ignore_index = True)

table_transposed = table_prepped.T
matches = count_matches(table_prepped.loc[table_prepped["PIVOT"].isnull()])
st.sidebar.write(state.r, " out of ", matches)
totalrows = len(table_prepped.index)



table_pivots = table_prepped.loc[(table_prepped['PIVOT'] == "PIVOT") | (table_prepped['PIVOT'] == "SIBLING")] 

table_new = pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "REMARKS", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
def tablePivots():    
    i = 0
    for index, row in table_pivots.iterrows():
        row.STEWARD_APPROVAL = "PIVOT"
        row.STEWARD = stewardName
        row.DATE_APPROVED = datetime.now()
        row.TIME_TAKEN = 0
        table_new.loc[i] = row
        i+=1
    else:
        return table_new

pivots = count_clusters(tablePivots())
totalpivots = len(table_pivots.index)
totalmatch = matches + totalpivots
totalclusters = pivots
def drawtable(tableout):
    st.table(tableout)
def prepmatches(matchid):
    table_matches = table_prepped.loc[(table_prepped["MATCH_ID"] == matchid) & (table_prepped["PIVOT"] != "PIVOT") & (table_prepped["PIVOT"] != "SIBLING")]
    i = 0
    table_matches_prepped =  pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "REMARKS", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
    
    for index, row in table_matches.iterrows():
        table_matches_prepped.loc[i] = row
        i+=1
    else:
        pass
    #prepmatches.count = count_matches(table_matches_prepped)
    return table_matches_prepped
def getcluster(clusterid):
    return state.tablout.loc[(state.tablout["CLUSTER_ID"] == clusterid)]
def get_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

def tableReports(tablout, rows, clusters, pivots, matches):
    finishdate = datetime.now()
    taken = tablout['TIME_TAKEN'].sum()
    data = [[finishdate, rows, clusters, pivots, matches, taken]]
    report = pd.DataFrame(data, columns=["DATE FINISHED", "ROWS", "CLUSTERS", "PIVOTS", "MATCHES", "TIME_TAKEN"])
    return report

table_OUT = table_prepped

while state.j < pivots:
    pivot = tablePivots().loc[state.j]
    matchid = pivot['RECORD_ID']
    table_matches = prepmatches(matchid)
    matchto = count_matches(table_matches)
    st.write('MATCH_ID: ', matchid, "    Match Count: ", matchto)
    proceed = ""
    while state.k < matchto:
        match = table_matches.loc[state.k]
        outable = pd.concat([pivot, match], axis = 1)
        st.write("Match iteration " + str(state.k))
 
        if approval =="":
            st.table(outable)
            
            ttaken = st.text("Time taken: " + str(state.taken))
            while approval == "":
                time.sleep(.5)
                state.t += 1
                state.taken += 0.5
                ttaken.text("Time taken: " + str(state.taken))
            else:
                
                pass
                
        else:
            modRow(match, approval, state.taken, remark)
            state.taken = 0
            approval = ""
            remark = ""
            state.k += 1
            state.r += 1
            
    else:
       
        if proceed == "":
            
            if st.button("Next"):
                proceed = "Next"
                state.j += 1
                state.k = 0
            else:        
                writePivot(pivot)
                clusterid = pivot.CLUSTER_ID
                st.markdown("""
                ## Cluster Review
                Press Next to proceed
                """)
                st.write(getcluster(clusterid))
                taken = 0
                waitmessage = st.text("Time taken: " + str(taken))
                while proceed == "":
                    time.sleep(0.5)
                    taken +=1
                    waitmessage.text("Time taken: " + str(taken))
                else:
                    pass
        else: 
            
            st.write(state.t)    
            st.write(state.j)
            
                 
else:
    st.write("All matches complete!")
    st.table(tableReports(state.tablout, totalrows, totalclusters, totalpivots, totalmatch))
    st.markdown(get_download(state.tablout), unsafe_allow_html=True)
    #PRINT OUT report data