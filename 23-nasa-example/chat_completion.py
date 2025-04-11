# Import libraries
from dotenv import load_dotenv  
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizableTextQuery
from azure.ai.inference.prompts import PromptTemplate
from openai import AzureOpenAI
from pathlib import Path

import re
import pathlib
import os

load_dotenv()

def setup() -> tuple:

    # Set up the Azure OpenAI client
    openai_client = AzureOpenAI(
        api_version="2024-05-01-preview",
        azure_endpoint=os.environ['AZURE_OPENAI_ACCOUNT'],
        api_key=os.environ['AZURE_OPENAI_KEY']
    )

    deployment_name = "DeepSeek-R1"

    # Set up the Azure Azure AI Search client
    search_client = SearchClient(
        endpoint=os.environ['AZURE_SEARCH_SERVICE'],
        index_name=os.environ['INDEX'],
        credential=DefaultAzureCredential()
    )
    return openai_client, search_client, deployment_name

def clean_text(text: str) -> str:
    # Remove quebras de linha, múltiplos espaços, tabs
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def search_index(search_client: SearchClient, query: str) -> dict:
    # It's hybrid: a keyword search on "query", with text-to-vector conversion for "vector_query".
    # The vector query finds 50 nearest neighbor matches in the search index
    vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")
    
    # Retrieve the selected fields from the search index related to the question.
    # Search results are limited to the top 3 matches. Limiting top can help you stay under LLM quotas.
    search_results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["chunk", "title", "locations"],
        top=3
    )

    documents=[
        {
            "title": doc["title"],
            "chunk": clean_text(doc["chunk"]),
            "locations": doc["locations"]
        }
        for doc in search_results
    ]

    return documents

def get_prompt() -> PromptTemplate:
    # Load the prompt template from the file
    ASSET_PATH = pathlib.Path(__file__).parent.resolve() / "assets"
    grounded_chat_prompt = PromptTemplate.from_prompty(Path(ASSET_PATH) / "grounded_chat.prompty")

    return grounded_chat_prompt


def main():
    return "__main__"

if main() == "__main__":
    print("This example demonstrates how to use the Azure OpenAI Service with Azure AI Search.")
    print("It uses a hybrid search approach, combining keyword search and vector search.")
    print("The search results are used to provide context for the chat model.")
    print("The chat model is used to generate a response based on the search results.")
    print("The search results are limited to the top 5 matches.")
    print("The vector query finds 50 nearest neighbor matches in the search index.\n\n")
    
    openai_client, search_client, deployment_name = setup()

    query = input("Digite a query:")
    user_messages=[{"role": "user", "content": query}]

    documents = search_index(search_client, query)

    print("=== Grounded Chat Example ===")
    grounded_chat_prompt = get_prompt()

    system_message = grounded_chat_prompt.create_messages(documents=documents, context=None)

    print(f"System message: {system_message}")
    print(f"User messages: {user_messages}")

    # Set up the chat thread.
    response = openai_client.chat.completions.create(
        messages=system_message + user_messages,
        model=deployment_name,
        **grounded_chat_prompt.parameters
    )

    print(response.choices[0].message.content)
