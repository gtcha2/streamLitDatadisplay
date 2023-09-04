import streamlit as st
import jsonschema2tree as j2t

# Title of the Streamlit app
st.title("JSON Tree Viewer")

# Create a file uploader to upload JSON data
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    try:
        # Read the uploaded JSON data
        data = json.load(uploaded_file)

        # Convert JSON data to a collapsible tree
        tree_data = j2t.convert(data)

        # Display the tree view of the JSON data
        st.write("## Explore JSON Data")
        st.write("Use the tree view below to explore the JSON data:")
        st.json(tree_data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
