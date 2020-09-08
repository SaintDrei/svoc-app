import streamlit as st
import pandas as pd
import numpy as np
import os
st.set_option('deprecation.showfileUploaderEncoding', False)


# Header
st.title("SVOC Data Steward Approval Tool")
st.write("Compare the values and press Reject or Approve accordingly")

# Sidebar
st.sidebar.subheader("Steward")
stewardlist = ["ADSantos", "ASRicamara", "KManingat", "LPalabay", "MAlvarado", "MMarcos", "RVillareal"]
option = st.sidebar.selectbox(
    'Select steward username',
     stewardlist)


st.sidebar.subheader("Upload CSV File")
file_CSV = st.sidebar.file_uploader("Drag file here or click browse files", type=["csv"])
table_CSV = pd.read_csv(file_CSV)
table_transposed = table_CSV.T
def color_dupes(x):
    c1='background-color:red'
    c2=''
    cond=x.stack().duplicated(keep=False).unstack()
    df1 = pd.DataFrame(np.where(cond,c1,c2),columns=x.columns,index=x.index)
    return df1
table_transposed.style.apply(color_dupes,axis=None, subset=['MATCH_ID', 'RECORD_ID'])

st.write(pd.DataFrame(table_transposed))
st.write(st.table(table_transposed))


remark = st.sidebar.text_input("Remarks", )
st.button("Approve") 
st.button("Reject")

#print(pd.DataFrame.equals(table_CSV))

# Sidebar - END

'You selected: ', option

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)