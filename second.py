import pandas as pd
import numpy as np
import streamlit as st


   



hellothere = ""

while hellothere != "Approve":
    hellothere = "heyo"
else:
    hellothere = "Hey"
    
st.write("hellothere")
if st.button("Approve", "apr"):
    hellothere = "Approve"
elif st.button("Reject", "rej"):
    hellothere =  "Reject"
else:
    hellothere = "Click something"

    hellothere = "DO something"
st.write(hellothere)