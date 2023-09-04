# Title of the Streamlit app
import streamlit as st
import json
st.title("JSON Data Viewer")

# Create a file uploader to upload JSON data
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    # Read the uploaded JSON data
    data = json.load(uploaded_file)

    # Display the JSON data in a code block
    st.code(json.dumps(data, indent=2), language='json')