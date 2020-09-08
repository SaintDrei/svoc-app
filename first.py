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
def prep_csv():
    try:
        table_CSV = pd.read_csv(file_CSV)
        table_transposed = table_CSV.T
        return table_transposed
    except:
        return st.write("""
        ## Please upload CSV on the sidebar
        """)

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
    st.write(st.table(prep_csv()))
    remark = st.text_input("Remarks", )
    timeApproved = datetime.now()
    st.write(timeApproved)
    st.button("<font color='green'>Approve</font>, unsafe_allow_html=True") 
    st.button("Reject")
except:
    st.write("ahh")


#print(pd.DataFrame.equals(table_CSV))

# Sidebar - END

