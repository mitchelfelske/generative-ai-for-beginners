from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexer
)

import os

load_dotenv()

skillset_name = "py-rag-tutorial-ss"
index_name = "py-rag-tutorial-idx"
data_source_name = "py-rag-tutorial-ds"

# Create an indexer  
indexer_name = "py-rag-tutorial-idxr" 
indexer_parameters = None

indexer = SearchIndexer(  
    name=indexer_name,  
    description="Indexer to index documents and generate embeddings",  
    skillset_name=skillset_name,  
    target_index_name=index_name,  
    data_source_name=data_source_name,
    parameters=indexer_parameters
)  

# Create and run the indexer  
indexer_client = SearchIndexerClient(endpoint=os.environ['AZURE_SEARCH_SERVICE'], credential=DefaultAzureCredential())  
indexer_result = indexer_client.create_or_update_indexer(indexer)  

indexer_client.run_indexer(indexer_name)
print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.') 

