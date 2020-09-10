import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time
import threading
import SessionState

st.set_option('deprecation.showfileUploaderEncoding', False)
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

def writeRow(row, approval, prev, table_OUT):   
    towrite =  table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID]
    towrite.STEWARD_APPROVAL = approval
    towrite.DATE_APPROVED = datetime.now()
    towrite.STEWARD = stewardName
    towrite.TIME_TAKEN = datetime.now() - prev
    st.write(towrite)
        
# Variables

table_prepped = prep_csv()
table_transposed = table_prepped.T
table_OUT = table_prepped
matches = count_matches(table_prepped)
st.sidebar.write("0 out of ", matches)

st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'

st.write("Num of rows", count_matches(table_prepped))

table_pivots = table_prepped.loc[(table_prepped['PIVOT'] == "PIVOT") | (table_prepped['PIVOT'] == "SIBLING")] 
data = [["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"]]

table_new = pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])

i = 0
for index, row in table_pivots.iterrows():
    table_new.loc[i] = row
    i+=1
else:
    pass

pivots = count_clusters(table_prepped)

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

#for index, row in table_pivots.iterrows():
 #   st.write(index, row)
  #  input(st.button("Continue"))
st.title("PIVOTS")
st.table(table_new)

state = SessionState.get(j = 0, t = 0,ta = 0, k = 0)
while state.j <= pivots:
    pivot = table_new.loc[state.j]
    st.table(pivot)
    #if approval == "":
    #    pass
    #else:
    #timebefore = time.time()
    matchid = pivot['MATCH_ID']
    st.write('matchid is', matchid)
    table_matches = prepmatches(matchid)
    matchto = count_matches(table_matches)
    st.write("matches are", matchto)
    st.table(table_matches)
    while state.k <= matchto:
        match = table_matches.loc[state.k]
        outable = pd.concat([pivot, match], axis = 1)
        st.table(outable)
        while approval == "":
            time.sleep(.5)
            state.t += 1
            st.write('approvee')
        else:
        #timebefore = statetime
            state.k += 1
            
        #timetaken = datetime.now().time() - timebefore
        
    else:
        state.j += 1
        st.write(state.j)
        st.write(state.t)
        
        
    approval=""        

    
   
    
else:
    st.write("Done")
