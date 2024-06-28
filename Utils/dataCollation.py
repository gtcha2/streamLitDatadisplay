import os
import json
import pandas as pd

#TODO: make csv_files more modular.

#


class DataCollator:
    def __init__(self, raw_data_dir, processed_data_dir):
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
        self.jsonl_files = [os.path.join(self.raw_data_dir, 'gpt4o_outputs_6_20', f) for f in os.listdir(os.path.join(self.raw_data_dir, 'gpt4o_outputs_6_20')) if f.endswith('.jsonl')]
        
        
        self.csv_files = [
            {'model_name': 'Llama 3', 'file_path': os.path.join(self.raw_data_dir, 'llama3_70B_2_20240624.csv')},
            {'model_name': 'LLAVA Llama 3', 'file_path': os.path.join(self.raw_data_dir, 'llava_llama3_multimodal_20240623.csv')}
        ]
        
        self.combined_csv_path = os.path.join(self.processed_data_dir, 'combined_model_outputs.csv')
    
    def load_jsonl_files(self):
        jsonl_data = []
        for file_path in self.jsonl_files:
            with open(file_path, 'r') as file:
                jsonl_data.extend([json.loads(line) for line in file])
        return jsonl_data
    
    def load_csv_file(self, file_path):
        return pd.read_csv(file_path)
    
    def transform_jsonl(self, data, output_key='response.body.choices[0].message.content'):

        transformed = []
        for entry in data:
            full_custom_id = entry.get('custom_id')
            subreddit, post_id, comment_index, _ = self._split_custom_id(full_custom_id)
            custom_id = f"{subreddit}_{post_id}_{comment_index}"
            model_name = entry['response']["body"]["model"]
            output = self._get_nested_value(entry, output_key)
            transformed.append({
                'custom_id': custom_id,
                'subreddit': subreddit,
                'post_id': post_id,
                'comment_index': comment_index,
                'model_name': model_name,
                'output': output
            })
        return transformed

    def _split_custom_id(self, custom_id):
        components = custom_id.split('_')
        subreddit = components[0]
        post_id = components[1]
        comment_index = components[2]
        date = components[3]
        return subreddit, post_id, comment_index, date
    
    def _get_nested_value(self, data, key):
        keys = key.split('.')
        for k in keys:
            if '[' in k and ']' in k:
                k, index = k.split('[')
                index = int(index[:-1])
                data = data[k][index]
            else:
                data = data[k]
        return data
    
    def transform_csv(self, data, model_name):
        transformed = []
        for _, row in data.iterrows():
            subreddit = row['subreddit']
            post_id = row['id']
            comment_index = row['comment_index']
            custom_id = f"{subreddit}_{post_id}_{comment_index}"
            output = row['outputs']
            transformed.append({
                'custom_id': custom_id,
                'subreddit': subreddit,
                'post_id': post_id,
                'comment_index': comment_index,
                'model_name': model_name,
                'output': output
            })
        return transformed
    
    def collate_data(self):
        jsonl_data = self.load_jsonl_files()
        jsonl_transformed = self.transform_jsonl(jsonl_data)

        all_csv_transformed = []
        for csv_info in self.csv_files:
            csv_data = self.load_csv_file(csv_info['file_path'])
            csv_transformed = self.transform_csv(csv_data, csv_info['model_name'])
            all_csv_transformed.extend(csv_transformed)

        all_data = jsonl_transformed + all_csv_transformed
        return all_data
    def save_data(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.combined_csv_path, index=False)
        print(f"Data saved to {self.combined_csv_path}")

if __name__ == "__main__":
    # Define paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_dir = os.path.join(project_root, 'data', 'raw')
    processed_data_dir = os.path.join(project_root, 'data', 'processed')

    # Initialize the DataCollator
    collator = DataCollator(raw_data_dir, processed_data_dir)
    
    # Collate the data
    all_data = collator.collate_data()
    
    # Print some of the results
    for entry in all_data[:5]:  # Print the first 5 entries
        print(entry)
    
    collator.save_data(all_data)
