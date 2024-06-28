
#FIXME please

def get_comments(data, subreddit, post_id):
    # Get the posts from the selected subreddit
    posts = data[subreddit]

    # Get the selected post
    post = next(post for post in posts if post['id'] == post_id)

    # Return the comments from the selected post
    return post['comments']
import json

def loadJSON(path):
    with open(path, 'r') as json_data:
        json_data_loaded=json.load(json_data)
    return json_data_loaded



# need function that takes in the following
#
# ok so you have to do the following tonight... you need to fix up the follwog k 
import json

def split_batches(json_objects, max_tokens_per_batch, tokens_per_request):
    max_requests_per_batch = max_tokens_per_batch // tokens_per_request
    batches = []
    current_batch = []

    for i, obj in enumerate(json_objects):
        current_batch.append(obj)
        if (i + 1) % max_requests_per_batch == 0:
            batches.append(current_batch)
            current_batch = []

    if current_batch:
        batches.append(current_batch)

    return batches

def write_batches_to_files(batches, base_filename):
    for i, batch in enumerate(batches):
        filename = f"{base_filename}_batch_{i+1}.jsonl"
        with open(filename, 'w') as outfile:
            for json_object in batch:
                json.dump(json_object, outfile)
                outfile.write('\n')
        print(f"Batch {i+1} written to {filename}")

# Load the JSON objects from the original JSONL file
file_path = '/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/batchedOutputs2.jsonl'
with open(file_path, 'r') as infile:
    json_objects = [json.loads(line) for line in infile]

# Define limits
max_tokens_per_batch = 1350000
tokens_per_request = 1800

# Split the requests into batches based on the token assumption
batches = split_batches(json_objects, max_tokens_per_batch, tokens_per_request)

# Write the batches to separate JSONL files
write_batches_to_files(batches, 'batchedOutputs2')

