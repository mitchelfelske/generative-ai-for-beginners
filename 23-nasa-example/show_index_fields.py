from dotenv import load_dotenv  
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex
from azure.identity import DefaultAzureCredential

import os

load_dotenv()

index_client = SearchIndexClient(endpoint=os.environ['AZURE_SEARCH_SERVICE'], credential=DefaultAzureCredential())
index = index_client.get_index("py-rag-tutorial-idx")

for field in index.fields:
    print(f"{field.name} ({field.type})")
