from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection
)

import os

load_dotenv()

indexer_client = SearchIndexerClient(
    endpoint=os.environ["AZURE_SEARCH_SERVICE"], 
    credential=DefaultAzureCredential()
)

# Creates a data source connection to the Azure Blob Storage container
# Intent: get pdfs from blob storage
# Container name: "nasa-ebooks-pdfs-all"
data_source_connection = SearchIndexerDataSourceConnection(
    name=os.environ['DATA_SOURCE'],
    type="azureblob",
    container=SearchIndexerDataContainer(name=os.environ["CONTAINER"]),
    connection_string=os.environ["AZURE_STORAGE_CONNECTION"]
)

data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)

print(f"Data source '{data_source.name}' created or updated")
