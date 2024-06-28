# Example: reuse your existing OpenAI setup
# rename this file to cleanup folder. 
from openai import OpenAI
import pandas as pd
# Point to the local server
df=pd.read_csv("llava_llama3_multimodal.csv")


client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
def runMessages(row):
    if not row["outputs"] is None and not pd.isna(row["outputs"]):
        
        completion = client.chat.completions.create(
        model="failspy/llama-3-70B-Instruct-abliterated-GGUF",
        messages=[
            {"role": "system", "content": "from the string only extract json, if erroneously formed try to fix and return json, else return empty json object"},
            {"role": "user", "content": row["outputs"]}
        ],
        response_format={ "type": "json_object", },

        temperature=0.2,
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    else:
        return None
df["clean_outcomes"] = df.apply(runMessages,axis=1)
df.to_csv("llava_llama3_multimodal_outputs_filtered.csv")
