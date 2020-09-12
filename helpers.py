import pandas as pd
import streamlit as st
import base64
from datetime import datetime


# VARIABLES


def prep_csv(file_csv):
    try:
        table_CSV = pd.read_csv(file_csv)        
        return table_CSV
    except:
        return st.markdown("<font color='red'><strong>Please upload CSV on the sidebar</strong></font>", unsafe_allow_html=True)
        
# COUNTERS
def count_clusters(x):
    counts = x["PIVOT"].value_counts()
    y = counts.iloc[0]
    return y

def count_matches(x):
    y = x["MATCH_ID"].value_counts()
    return y.sum(axis=0)


# WRITE ROWS
def writePivot(pivot, tablout, steward):
    pivot.STEWARD = steward
    pivot.DATE_APPROVED = datetime.now()
    pivot.STEWARD_APPROVAL = "PIVOT"
    tablout = tablout.append(pivot, ignore_index=True)

def modRow(record, approval, taken, steward, tablout):
    record.STEWARD = steward
    record.DATE_APPROVED = datetime.now()
    record.STEWARD_APPROVAL = approval
    record.TIME_TAKEN = taken
    tablout = tablout.append(record, ignore_index = True)


def get_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'


def drawtable(tableout):
    st.table(tableout)


#TABLES
data = [["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"]]
    
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

def tableCluster(clusterid, tablout):
    return tablout.loc[(tablout["CLUSTER_ID"] == clusterid)]


def tableMatches(matchid, table_prepped):
    table_matches = table_prepped.loc[(table_prepped["MATCH_ID"] == matchid) & (table_prepped["PIVOT"] != "PIVOT") & (table_prepped["PIVOT"] != "SIBLING")]
    table_matches_prepped =  pd.DataFrame(data, columns=["CLUSTER_ID","MATCH_ID",	"RECORD_ID", "PIVOT", "MATCH_COUNT", "LAST_NAME", "MIDDLE_INITIAL", "FIRST_NAME",	"COMPLETE_ADDRESS",	"SEX",	"BIRTHDATE", "MOBILE_NUMBER", "EMAIL", "TIN", "STEWARD", "STEWARD_APPROVAL", "APPROVAL_COUNT", "DATE_APPROVED", "TIME_TAKEN", "APPROVER", "SECOND_APPROVAL_DATE"])
    
    for index, row in table_matches.iterrows():
        table_matches_prepped.loc[index] = row
        
    else:
        pass
    #prepmatches.count = count_matches(table_matches_prepped)
    return table_matches_prepped

def tableReports(tablout, rows, clusters, pivots, matches):
    taken = tablout['TIME_TAKEN'].sum()
    data = [[rows, clusters, pivots, matches, taken]]
    report = pd.DataFrame(data, columns=["ROWS", "CLUSTERS", "PIVOTS", "MATCHES", "TIME_TAKEN"])
    return report


# RENDERS