from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT'],
    api_key= os.environ['AZURE_OPENAI_API_KEY'],
    api_version= os.environ['AZURE_OPENAI_API_VERSION']
)

deployment = os.environ['AZURE_OPENAI_DEPLOYMENT']

prompt = "Complete the following: Once upon a time there was a"
messages = [{"role": "user", "content": prompt}]

completion = client.chat.completions.create(model=deployment, messages=messages)

print(completion.choices[0].message.content)
