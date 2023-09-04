import streamlit as st
import json
from treelib import Tree

# Recursive function to build a tree structure from nested JSON
def build_tree(data, parent=None, tree=None):
    if tree is None:
        tree = Tree()
        parent = "root"  # Initialize parent to "root" for the root node
    
    try:
        if isinstance(data, dict):
            for key, value in data.items():
                node_id = parent + f"_{key}"
                tree.create_node(key, node_id, parent=parent, data=value)
                build_tree(value, parent=node_id, tree=tree)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                node_id = parent + f"_{i}"
                tree.create_node(f"[{i}]", node_id, parent=parent, data=item)
                build_tree(item, parent=node_id, tree=tree)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Title of the Streamlit app
st.title("JSON Data Explorer")

# Create a file uploader to upload JSON data
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    try:
        # Read the uploaded JSON data
        data = json.load(uploaded_file)

        # Build a tree structure from the JSON data
        data_tree = build_tree(data)
        
        # Display the tree view of the JSON data
        st.write("## Explore JSON Data")
        st.write("Use the tree view below to explore the JSON data:")
        st.write(data_tree.show(show_root=False))
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
