import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = "<API_ENDPOINT>"
deployment = "<MODEL_NAME>"

subscription_key = "<API_KEY>"
api_version = "<API_VERSION>"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_tokens=512,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)
