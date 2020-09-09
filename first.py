import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time


st.set_option('deprecation.showfileUploaderEncoding', False)
# Sidebar
st.sidebar.subheader("Steward")
stewardlist = ["ADSantos", "ASRicamara", "KManingat", "LPalabay", "MAlvarado", "MMarcos", "RVillareal"]
stewardName = st.sidebar.selectbox(
    'Select steward username',
     stewardlist)

 
st.sidebar.subheader("Upload CSV File")
file_CSV = st.sidebar.file_uploader("Drag file here or click browse files", type=["csv"])

st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'
def prep_csv():
    try:
        table_CSV = pd.read_csv(file_CSV)        
        return table_CSV
    except:
        return st.markdown("<font color='red'><strong>Please upload CSV on the sidebar</strong></font>", unsafe_allow_html=True)
        

table_prepped = prep_csv()
table_transposed = table_prepped.T
table_OUT = table_prepped

def count_clusters(x):
    counts = x["PIVOT"].value_counts()
    y = counts.iloc[0]
    return y

def count_matches(x):
    y = x["MATCH_ID"].value_counts()
    return y.sum(axis=0)

# def update_row(x, y, z):


def showview(x):
    st.write(st.table(x))
   # showButtons()

def showButtons():
    #remarks = st.text_input("Remarks", )
    timeApproved = datetime.now()
    st.write(timeApproved)
    if st.button("Approve"):
        return "Approve"
    if st.button("Reject"):
        return "Reject"
    
#def writeRow(row, approval, prev, table_OUT):    
 #   row.loc['STEWARD_APPROVAL'] = approval
  #  row.loc['DATE_APPROVED'] = datetime.now()
   # row.loc['STEWARD'] = stewardName
    #row.loc['TIME_TAKEN'] = datetime.now() - prev
    #st.write(table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID])
    #table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID] = row
    #st.write('test', row)

def writeRow(row, approval, prev, table_OUT):   
    towrite =  table_OUT.loc[table_OUT['RECORD_ID'] == row.RECORD_ID]
    towrite.STEWARD_APPROVAL = approval
    towrite.DATE_APPROVED = datetime.now()
    towrite.STEWARD = stewardName
    towrite.TIME_TAKEN = datetime.now() - prev
    st.write(towrite)
        
def passapproval()
    

st.write(count_matches(table_prepped))

st.write(table_prepped["MATCH_ID"].value_counts())

#for x in count_clusters(table_prepped):
    #st.write(x)
st.write('testing table pivots')
table_pivots = table_prepped.loc[(table_prepped['PIVOT'] == "PIVOT") | (table_prepped['PIVOT'] == "SIBLING")] 
for index, row in table_pivots.iterrows():
    st.write(index, row)
    x = table_prepped['MATCH_ID']
    table_comp = table_prepped.loc[(x == row["MATCH_ID"]) & (table_prepped["PIVOT"] != "PIVOT") & (table_prepped["PIVOT"] != "SIBLING") ]    
    pasdt = row
    st.table(table_comp.T)
    for index, row in table_comp.iterrows():
        st.write("match", index)
        outable = pd.concat([pasdt, row], axis=1)
        st.write(row.loc['RECORD_ID'])
        st.write("Compare the values and press Reject or Approve accordingly")
        prev = datetime.now()
        showview(outable)
        approval = ""
        while approval =="":

        writeRow(row, showButtons(), prev, table_OUT)

        st.write("End of match", index)
        #if showview(outable) == "1":
        #    continue
        #return next(row)
    else:
        break

else: 
    st.write("Finished")

st.write("end test")
st.table(table_pivots.T)
#st.write(table_prepped[table_prepped>=1].sum(axis=4))    
#st.write(count_clusters(table_prepped))
# Header
st.title("SVOC Data Steward Approval Tool")
'Welcome ', stewardName, '!'
st.write("Compare the values and press Reject or Approve accordingly")


#def color_dupes(x):
#    c1='background-color:red'
#    c2=''
#    cond=x.stack().duplicated(keep=False).unstack()
#    df1 = pd.DataFrame(np.where(cond,c1,c2),columns=x.columns,index=x.index)
#    return df1
#table_transposed.style.apply(color_dupes,axis=None, subset=['MATCH_ID', 'RECORD_ID'])


try:
    showview(table_transposed)
    st.write(table_transposed["PIVOT"].value_counts())
except:
    st.write("ahh")

st.write("Table OUT")
st.table(table_OUT)
#print(pd.DataFrame.equals(table_CSV))

# Sidebar - END

