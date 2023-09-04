import streamlit as st
import json
from jsonschema import validate

# Title of the Streamlit app
st.title("JSON Tree Viewer")

# Create a file uploader to upload JSON data
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    try:
        # Read the uploaded JSON data
        data = json.load(uploaded_file)

        # Display the tree view of the JSON data
        st.write("## Explore JSON Data")
        st.write("Use the tree view below to explore the JSON data:")

        # Define a recursive function to display JSON data in a collapsible format
        def display_json(data, parent="root"):
            for key, value in data.items():
                if isinstance(value, dict):
                    st.json({key: display_json(value, key)})
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        st.json({f"{key}[{i}]": display_json(item, f"{key}[{i}]")})
                else:
                    st.text(f"{key}: {value}")

        display_json(data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
