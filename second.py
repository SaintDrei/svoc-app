import pandas as pd
import numpy as np
import streamlit as st


   



hellothere = ""
counter = 0

if st.sidebar.button("Approve", "apr"):
    hellothere = "Approve"
elif st.sidebar.button("Reject", "rej"):
    hellothere =  "Reject"
else:
    pass

st.write(hellothere)


while hellothere == "":
    counter += 1
    
    st.write(hellothere, counter)
    
else:
    st.write(hellothere)
    st.write("Hayoo")
    counter = counter