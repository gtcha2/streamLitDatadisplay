


import pandas as pd
import os
import json
from collections import defaultdict



class JSONLHandler:
    def __init__(self):
        self.data = []

    def load_file(self, file_path):
        """Loads a JSONL file and appends its contents to the data list."""
        with open(file_path, 'r') as file:
            for line in file:
                json_obj = json.loads(line)
                self.data.append(json_obj)

    def save_to_file(self, file_path):
        """Saves the contents of the data list to a JSONL file."""
        with open(file_path, 'w') as file:
            for json_obj in self.data:
                file.write(json.dumps(json_obj) + '\n')

    def get_data(self):
        """Returns the data list containing all JSON objects."""
        return self.data

    def load_multiple_files(self, file_paths):
        """Loads multiple JSONL files and appends their contents to the data list."""
        for file_path in file_paths:
            self.load_file(file_path)

    def load_from_directory(self, directory_path):
        """Loads all JSONL files in a given directory and appends their contents to the data list."""
        for filename in os.listdir(directory_path):
            if filename.endswith('.jsonl'):
                
                self.load_file(os.path.join(directory_path, filename))

# Example usage:
handler = JSONLHandler()

# List and load all JSONL files in a directory
directory_path = '/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/GPT4o_outputs_6_20'
handler.load_from_directory(directory_path)
# handler.load_file("/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/GPT4_outputs_batched/batch_wTZsiBGVQEfo0cMHMLARtsbn_output_gpt4o_batch_25.jsonl")
# Get all loaded data as a list of JSON objects
all_data = handler.get_data()

# Save the combined data to a new JSONL file
# combined_file_path = 'combined.jsonl'
# handler.save_to_file(combined_file_path)


# so with the combined data you need to do the stats on the following... you need to build the possible
import json
import re


class JSONExtractor:
    def __init__(self):
        self.extracted_data = []

    def extract_from_string(self, string):
        """Extracts valid JSON objects from a string and appends them to extracted_data."""
        json_objects = self._find_json_objects_in_string(string)
        for json_obj in json_objects:
            try:
                parsed_json = json.loads(json_obj)
                self.extracted_data.append(parsed_json)
            except json.JSONDecodeError:
                pass  # Skip invalid JSON

    def get_extracted_data(self):
        """Returns the list of extracted JSON objects."""
        return self.extracted_data

    def _find_json_objects_in_string(self, string):
        """Finds all potential JSON objects in a string, including multiline JSON."""
        json_objects = []
        brace_level = 0
        json_start = -1

        for i, char in enumerate(string):
            if char == '{':
                if brace_level == 0:
                    json_start = i
                brace_level += 1
            elif char == '}':
                brace_level -= 1
                if brace_level == 0:
                    json_objects.append(string[json_start:i+1])

        return json_objects

# Test the JSONExtractor


# Test the JSONExtractor
def extract_and_order_keys_by_frequency(data):
    extractor = JSONExtractor()
    key_frequency = defaultdict(int)
    
    for item in data:
        try:
            content = item['response']["body"]["choices"][0]["message"]["content"]
            extractor.extract_from_string(content)
            extracted_data = extractor.get_extracted_data()
            for json_obj in extracted_data:
                for key in json_obj.keys():
                    key_frequency[key] += 1
            extractor.extracted_data.clear()  # Clear extractor's data for the next item
        except KeyError:
            # Skip if the expected structure is not present
            continue

    # Sort keys by frequency
    sorted_keys_by_frequency = sorted(key_frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_keys_by_frequency

# Extract and order keys by frequency
print(len(all_data))


#set up dataframe with the following information, 1: the custom_id extract the date. this is from the custom id, split the last 6 digits into
# into the date column,.... next up 
print(all_data[0].keys())
sorted_keys_by_frequency = extract_and_order_keys_by_frequency(all_data)
print(sorted_keys_by_frequency)
# # jsonExtract=JSONExtractor()
# jsonExtract.extract_from_string(all_data[5]['response']["body"]["choices"][0]["message"]["content"])
# print(all_data[5]['response']["body"]["choices"][0]["message"]["content"])
# print(jsonExtract.get_extracted_data()[0].keys())

# combine everything into one docuemnt.
# 

