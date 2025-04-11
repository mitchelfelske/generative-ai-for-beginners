from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexer
)

import os

load_dotenv()

# Create an indexer  
indexer_name = os.environ["INDEXER"] 
indexer_parameters = None

indexer = SearchIndexer(  
    name=indexer_name,  
    description="Indexer to index documents and generate embeddings",  
    skillset_name=os.environ['SKILLSET'],  
    target_index_name=os.environ['INDEX'],  
    data_source_name=os.environ['DATA_SOURCE'],
    parameters=indexer_parameters
)  

# Create and run the indexer  
indexer_client = SearchIndexerClient(endpoint=os.environ['AZURE_SEARCH_SERVICE'], credential=DefaultAzureCredential())  
indexer_result = indexer_client.create_or_update_indexer(indexer)  

indexer_client.run_indexer(indexer_name)
print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.') 

