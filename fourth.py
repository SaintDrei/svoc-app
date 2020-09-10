import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time
import threading
import SessionState

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
def prep_csv():
    try:
        table_CSV = pd.read_csv(file_CSV)        
        return table_CSV
    except:
        return st.markdown("<font color='red'><strong>Please upload CSV on the sidebar</strong></font>", unsafe_allow_html=True)
        

def count_clusters(x):
    counts = x["PIVOT"].value_counts()
    y = counts.iloc[0]
    return y

def count_matches(x):
    y = x["MATCH_ID"].value_counts()
    return y.sum(axis=0)



        
# Variables

table_prepped = prep_csv()
state = SessionState.get(j = 0, t = 0,ta = 0, k = 0, r = 0, tablout = pd.DataFrame())
if state.tablout is None:
    state.tablout = table_prepped
else:
    st.write("tablout is written")
    st.write(state.tablout)
def writeRow(row, approval, prev, table_OUT):   
    towrite =  table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID]
    towrite.STEWARD_APPROVAL = approval
    towrite.DATE_APPROVED = datetime.now()
    towrite.STEWARD = stewardName
    towrite.TIME_TAKEN = datetime.now() - prev
    st.write(towrite)


@st.cache(allow_output_mutation=True)
def getTabl():
    return pd.DataFrame()

def writePivot(pivot, steward):
    pivot.STEWARD = steward
    pivot.DATE_APPROVED = datetime.now()
    pivot.STEWARD_APPROVAL = "PIVOT"
    #pivot.loc['STEWARD'] = steward
    #pivot.loc['DATE_APPROVED'] = datetime.now()
    #pivot.loc['STEWARD_APPROVAL'] = "PIVOT"
    #"STEWARD":steward, "DATE_APPROVED":datetime.now(), 'STEWARD_APPROVAL': "PIVOT"}
    #getTabl().append(pivot, ignore_index=True)
    #getTabl().append("shark":"sharks", ignore_index=True)
    #pd.concat([getTabl(), pivot], axis=1)
    
    state.tablout = state.tablout.append(pivot, ignore_index=True)
    

def modRow(steward, record, approval, prev):
    record.loc['STEWARD'] = steward
    record.loc['DATE_APPROVED'] = datetime.now()
    
table_transposed = table_prepped.T
matches = count_matches(table_prepped.loc[table_prepped["PIVOT"].isnull()])
st.sidebar.write(state.r, " out of ", matches)
totalrows = len(table_prepped.index)
st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'


table_pivots = table_prepped.loc[(table_prepped['PIVOT'] == "PIVOT") | (table_prepped['PIVOT'] == "SIBLING")] 

table_new = pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])

i = 0
for index, row in table_pivots.iterrows():
    table_new.loc[i] = row
    i+=1
else:
    pass

pivots = count_clusters(table_prepped)
totalpivots = len(table_pivots.index)
totalmatch = matches + totalpivots
totalclusters = pivots
def drawtable(tableout):
    st.table(tableout)
def prepmatches(matchid):
    table_matches = table_prepped.loc[(table_prepped["MATCH_ID"] == matchid) & (table_prepped["PIVOT"] != "PIVOT") & (table_prepped["PIVOT"] != "SIBLING")]
    i = 0
    table_matches_prepped =  pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
    
    for index, row in table_matches.iterrows():
        table_matches_prepped.loc[i] = row
        i+=1
    else:
        pass
    #prepmatches.count = count_matches(table_matches_prepped)
    return table_matches_prepped
table_OUT = table_prepped

while state.j <= pivots:
    pivot = table_new.loc[state.j]
    matchid = pivot['MATCH_ID']
    table_matches = prepmatches(matchid)
    matchto = count_matches(table_matches)
    st.write('MATCH_ID: ', matchid, "    Match Count: ", matchto)
    timeprev = datetime.now()
    writePivot(pivot, stewardName)
    st.write(state.tablout)
    while state.k < matchto:
        match = table_matches.loc[state.k]
        outable = pd.concat([pivot, match], axis = 1)
        st.write(outable)
        state.tablout.append({"stuff":"stuff"}, ignore_index=True)
        st.write("stuff")
        st.write(state.tablout)
        #drawtable(outable)
        #st.table(state.tablout)
        while approval == "":
            time.sleep(.5)
            state.t += 1
            st.write(state.t)
        else:
           # writeRow(match, approval, timeprev, state.tablout)
            approval = ""
            state.k += 1
            state.r += 1
            
            
    else:
        state.j += 1
        state.k = 0
        st.write(state.j)
        st.write(state.t)
        #INsert review block
        break
               
    approval=""     
else:
    st.write("Done")
