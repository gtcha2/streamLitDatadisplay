# import json
# import re
# import pandas as pd
# def safe_extract_key_value_pairs(input_string):
#     """
#     Attempts to extract key-value pairs from corrupted JSON-like strings.
#     Returns an empty dictionary if parsing fails.
#     """
#     try:
#         # Clean the input string to remove extraneous characters
#         cleaned_input = re.sub(r'[^0-9,:{}\[\]"\'-]', ' ', input_string)
#         cleaned_input = re.sub(r'\s+', ' ', cleaned_input)
#         cleaned_input = cleaned_input.replace('{ ', '{').replace(' }', '}').replace(' :', ':').replace(': ', ':')

#         # Parse cleaned input as JSON
#         potential_json = json.loads(cleaned_input)

#         # Extract only the numeric key-value pairs
#         filtered_json = {int(k): int(v) for k, v in potential_json.items() if isinstance(v, (int, float))}
#         return filtered_json

#     except Exception:
#         # Return an empty dictionary if any error occurs
#         return None


# # Load the dataset
# data = pd.read_csv('data/processed/combined_model_outputs.csv')

# # Apply the function to the 'output' column
# data['extracted_json'] = data['output'].apply(safe_extract_key_value_pairs)

# # Save the results to a new CSV file
# data.to_csv('data/processed/stripped_model_outputs.csv', index=False)
import pandas as pd
import json
import re

def extract_gpt4_json(input_string):
    try:
        # Clean the input string to remove extraneous characters
        cleaned_input = re.sub(r'[^0-9,:{}\[\]"\'-]', ' ', input_string)
        cleaned_input = re.sub(r'\s+', ' ', cleaned_input)
        cleaned_input = cleaned_input.replace('{ ', '{').replace(' }', '}').replace(' :', ':').replace(': ', ':')

        # Parse cleaned input as JSON
        potential_json = json.loads(cleaned_input)

        # Extract only the numeric key-value pairs
        filtered_json = {int(k): int(v) for k, v in potential_json.items() if isinstance(v, (int, float))}
        return filtered_json

    except Exception:
        # Return an empty dictionary if any error occurs
        return None

def extract_llama_json(input_string):
    """
    Extracts key-value pairs from Llama model outputs, ensuring numeric keys are quoted.
    Enhanced to handle non-standard characters, syntax such as code block markers, and extraneous data.
    Returns None if parsing fails.
    """
    try:
        # Remove Markdown code block markers
        cleaned_input = re.sub(r'```.*?\n', '', input_string)
        cleaned_input = re.sub(r'\s+', '', cleaned_input)

        # Find the first complete JSON object and ignore anything after it
        match = re.search(r'\{.*?\}', cleaned_input)
        if match:
            cleaned_input = match.group(0)

        # Add quotes around numeric keys
        cleaned_input = re.sub(r'(?<!")(\b\d+\b)(?!"):', r'"\1":', cleaned_input)
        cleaned_input = f'[{cleaned_input}]'  # Wrap in list if not already
        potential_json = json.loads(cleaned_input)

        # Extract key-value pairs, ensuring they are numeric
        result = {}
        if isinstance(potential_json, list):
            for item in potential_json:
                result.update({k: v for k, v in item.items() if isinstance(v, (int, float))})
        else:
            result = {k: v for k, v in potential_json.items() if isinstance(v, (int, float))}

        return result if result else None
    except Exception as e:
        return None

def extract_json_based_on_model(model_name, output_string):
    """
    Determines which extraction function to use based on the model name.
    """
    if 'llama' in model_name.lower():
        return extract_llama_json(output_string)
    else:
        return extract_gpt4_json(output_string)

# Example usage:
data = pd.read_csv('data/processed/combined_model_outputs.csv')
data['extracted_json'] = data.apply(lambda row: extract_json_based_on_model(row['model_name'], row['output']), axis=1)
data.to_csv('data/processed/stripped_model_outputs.csv', index=False)


# ok with this extraction I have to do what?
#
# the following should be done in this case... I need to update the following information 