# Example: reuse your existing OpenAI setup
# from openai import OpenAI

# # Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# completion = client.chat.completions.create(
#   model="failspy/llama-3-70B-Instruct-abliterated-GGUF",
#   messages=[
#     {"role": "system", "content": "Always answer in rhymes."},
#     {"role": "user", "content": "Introduce yourself."}
#   ],
#   temperature=0.7,
# )
# Adapted from OpenAI's Vision example 

## need to create unit tests for promptingServer:


from openai import OpenAI
import base64
import requests
import pandas as pd
from tqdm import tqdm
import ast
tqdm.pandas()
df = pd.read_csv("/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/filtered_misinformation_data.csv")
# Point to the local server


def display_comments(comment, level, parent_comment_author):
    indent = "\t" * level  # Indentation using tabs
    comment_text = f"{indent}**{comment.get('author')}** (Reply to {parent_comment_author}):\n"
    comment_text += f"{indent}{comment.get('body')}\n"
    for reply in comment.get('replies'):
        if reply != "[removed]":
            comment_text += display_comments(reply, level + 1, comment.get('author'))
    return comment_text


def postText(random_post,seperate=False):
    selfText=random_post.get('selftext',"")
    title=random_post.get('title',"")
    if pd.isna(selfText):
        selfText = ''

    if pd.isna(title):
        title = ''

    post_text_solo = "Post Content: " +"\n"+title+"\n" + selfText 
    post_text = "Post Content: " +"\n"+title+"\n" + selfText + "\n\nComments:\n"
    comment_text_solo = ""
    for comment in random_post.get('comments'):
        text2Add = display_comments(comment, level=0, parent_comment_author=random_post.get('author'))
        post_text+=text2Add
        comment_text_solo += text2Add

    if seperate:
      return post_text_solo,comment_text_solo
    else:

      return post_text
def promptBuilder(redditPostText,commentChainText):
  prompt = f"""
**Task: Evaluating Misinformation in Reddit Posts and Comments**

**Instructions:**
Evaluate the accuracy of the provided Reddit post and the responses provided by commenters regarding the topic of misinformation. Use required scale for each question. 

**Scale for questions 1-5:**
- 1: Strongly Disagree
- 2: Disagree
- 3: Neutral
- 4: Agree
- 5: Strongly Agree

**Scale for questions 6-8:**
- A number between 1-100

**Reddit Post:**
{redditPostText}

**Comment Chain:**
{commentChainText}

**Questions:**

1. To the best of your knowledge, is the answer to the post truthful?
2. Is the answer to the information harmful?
3. Does this response come from supported information?
4. Does this response answer the initial question?
5. Does the response show evidence of reasoning?

6. How confident are you in the accuracy of the information presented in the Reddit post?
7. How confident are you in the accuracy of the information provided by the commenters?
8. Overall, how reliable do you believe the Reddit post and the commenters' responses are in addressing misinformation? 

**Submission:**
Only provide your evaluation in the form of a JSON dictionary with question numbers as keys and scale responses as values. For example:

'''
{{
    1: 3,  # Example response for Question 1
    2: 4,  # Example response for Question 2
    3: 2,  # Example response for Question 3
    4: 5,  # Example response for Question 4
    5: 3,  # Example response for Question 5
    6: 90,  # Example response for Question 6
    7: 80,  # Example response for Question 7
    8: 85   # Example response for Question 8
}}
'''
"""

#   prompt = 
# f"""
#   **Task: Evaluating Misinformation in Reddit Posts and Comments**

#   **Instructions:**
#   Evaluate the accuracy of the provided Reddit post and the responses provided by commenters regarding the topic of misinformation. Use a Likert scale (1-5) for each question, with 1 being "Strongly Disagree" and 5 being "Strongly Agree." Provide your confidence level for each question in the form of a dictionary.

#   **Scale for questions 1-5:**
#   - 1: Strongly Disagree
#   - 2: Disagree
#   - 3: Neutral
#   - 4: Agree
#   - 5: Strongly Agree
#   **Scale for questions 6-8"

#   **Reddit Post:**
#     {redditPostText}

#   **Comment Chain:**
#     {commentChainText}

#   **Questions:**

#   1. To the best of your knowledge is the answer to the post truthful?
#   2. Is the answer to the information harmful?
#   3. Does this response come from supported information?
#   4. Does this response answer the initial question?
#   5. Does the response show evidence of reasoning?

#   6. How confident are you in the accuracy of the information presented in the Reddit post?
#   7. How confident are you in the accuracy of the information provided by the commenters?
#   8. Overall, how reliable do you believe the Reddit post and the commenters' responses are in addressing misinformation?(A number betwen 1-100)


#   **Submission:**
#   Only provide your evaluation in the form of a json dictionary with question numbers as keys and Likert scale responses (1-5) as values. For example:

#   '''
#   {{
#       1: 3,  # Example response for Question 1
#       2: 4,  # Example response for Question 2
#       # Include responses for all questions
#   }}'''
#   """

  return prompt
#    
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
def url_to_base64(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        else:
            return None
    except requests.exceptions.RequestException:
        return None
# first you need to create the 
filtered_subset=df[(df['post_hint'] != 'image') & ~(df['has_thumbnail'])]


# df['base64'] = df.apply(lambda row: url_to_base64(row['thumbnail']) if row['status'] == 'Exists' else None, axis=1)

df['unique_ID'] = df['subreddit'].astype(str) + '_' + df['id'].astype(str) + '_' + df['comment_index'].astype(str)

# data_dict = df.to_dict(orient='records')
filtered_subset=df[(df['post_hint'] != 'image') & ~(df['has_thumbnail'])]
data_dict = filtered_subset.to_dict(orient='records')



# Step 3: Define a recursive function to handle nested structures and parse JSON strings
def convert_nested(element):
    if isinstance(element, str):
        try:
            # Check if element is intended to be a dictionary or list
            if (element.startswith('{') and element.endswith('}')) or (element.startswith('[') and element.endswith(']') and element not in ["[removed]","[deleted]"]):
                return convert_nested(ast.literal_eval(element))
            else:
                return element
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing element: {element}\nError: {e}")
            return element
    elif isinstance(element, list):
        return [convert_nested(item) for item in element]
    elif isinstance(element, dict):
        return {key: convert_nested(value) for key, value in element.items()}
    else:
        return element
    
data_dict = [convert_nested(item) for item in data_dict]




def create_prompt_with_text(row,image=True,base64=True):
    Post,commentText=postText(row,True)

    finalText=promptBuilder(Post,commentText)
    if image:
        if base64:
            return {
                "role": "user",
                "content": [
                    {"type": "text", "text": finalText},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{row['base64']}"
                        },
                    },
                ],
            }
        else:
            return {
                "role": "user",
                "content": [
                    {"type": "text", "text": finalText},
                    {
                        "type": "image_url",
                        "image_url":{"url":row["thumbnail"]}
                        
                    },
                ],
            }

    else:
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": finalText}
                
            ]
        }

# this runs the code to create the message and stream 


def promptCreatorWithoutImages(row):

    prompt = create_prompt_with_text(row,False)
    # Example: reuse your existing OpenAI setup


# Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
    model="failspy/llama-3-70B-Instruct-abliterated-GGUF",
     messages=[
            {
                "role": "system",
                "content": "This is a chat between a user and an assistant. The assistant is helping the user accomplish a task with associated image information. Return only JSON",
            },
            prompt
        ], response_format={ "type": "json_object" },
    )


    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def promptCreator(row):
    ## need to change the create prompt to include the base64_image
    
    prompt = create_prompt_with_text(row)
    completion = client.chat.completions.create(
        model="xtuner/llava-llama-3-8b-v1_1-gguf",

        messages=[
            {
                "role": "system",
                "content": "This is a chat between a user and an assistant. The assistant is helping the user accomplish a task with associated image information. Return only JSON",
            },
            prompt
        ],
        response_format={ "type": "json_object" },
        stream=True,
        max_tokens=1000
    )
    description = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            description += chunk.choices[0].delta.content
    print(description)
    return description

from datetime import datetime

def runVisionModel(df,data_dict):
    current_datetime = datetime.now().strftime("%Y%m%d")
    # this works for all the data in vision outputs
    df['outputs'] = list(map(promptCreator,data_dict))
    # df['description'] = df['base64'].apply(lambda b64: get_image_description(b64) if b64 else None)

    # Display the updated DataFrame
    # print(df['description'])
    print(df['outputs'])
    df.to_csv(f"llava_llama3_multimodal_{current_datetime}.csv")
    return
def run_languageModel(df, data_dict):
    df['outputs'] = list(map(promptCreatorWithoutImages,data_dict))
    # df['description'] = df['base64'].apply(lambda b64: get_image_description(b64) if b64 else None)
    current_datetime = datetime.now().strftime("%Y%m%d")
    # Display the updated DataFrame
    # print(df['description'])
    print(df['outputs'])
    df.to_csv(f"llama3_70B_2_{current_datetime}.csv")
   
    return



run_languageModel(filtered_subset,data_dict)

# you need to be building things that can go from command line. 
def buildBatch(row):
    # goal o fthis function is to return a jsonL file in the form of custom_id, method,url,body={model, response_format, messages}
    # 
    #setup 
    
    current_datetime = datetime.now().strftime("%Y%m%d")
    custom_id = f"{row['unique_ID']}_{current_datetime}"
 
    method="POST"
    url="/v1/chat/completions"
    model = "gpt-4o"
    if row["status"] == "Exists":
        
        requestBody=create_prompt_with_text(row,True,False)
    elif row['post_hint'] != 'image'and not row['has_thumbnail']:
        
        requestBody=create_prompt_with_text(row,False,False)
    # what else needs to be accomplished, ok you have the request body supposedly?
    else: 
        return None
    messages = [
            {
                "role": "system",
                "content": "This is a chat between a user and an assistant. The assistant is helping the user accomplish a task with any associated information. Return only JSON",
            },
            requestBody
        ]
    jsonObject={ "custom_id":custom_id,
                "method":method,
                "url":url,
                "body":{
                    "model":model,
                    "messages":messages,

                    "response_format":{ "type": "json_object", }
                    ,
                    "max_tokens":1000,
                    "logprobs":True,
                    "top_logprobs":5}
                    }

    # ok so here we go, for each entry, you either have EXISTS or not... if exists, then you go down image path
    # if not, then you check if row 
    return jsonObject

"""
stps: 
1: get api key to make sure you are doing the appropriate thing.s 


"""

# clean up and put into code. 
# import json
# outcome = list(filter(None, map(buildBatch, data_dict)))
# with open('batchedOutputs2.jsonl', 'w') as outfile:
#     for json_object in outcome:
#         json.dump(json_object, outfile)
#         outfile.write('\n')
# runVisionModel(df,data_dict)
