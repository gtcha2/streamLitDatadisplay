import streamlit as st
import json
import pandas as pd

# Recursive function to flatten nested JSON objects
def flatten_json(y):
    """Flatten a nested JSON structure"""
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Title of the Streamlit app
st.title("JSON Data Viewer")

# Create a file uploader to upload JSON data
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    # Read the uploaded JSON data
    data = json.load(uploaded_file)

    # Flatten the JSON data
    flat_data = flatten_json(data)

    # Convert the flattened data to a DataFrame
    df = pd.DataFrame([flat_data])

    # Display the DataFrame as a table
    st.write(df)
