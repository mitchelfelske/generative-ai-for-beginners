from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

import os
from dotenv import load_dotenv

load_dotenv()

# Container name
container_name = "nasa-ebooks-pdfs-all"

# Get connection string from environment variable
connection_string = os.getenv("AZURE_STORAGE_CONNECTION")

# Creates the blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Lists the blobs in the container
container_client = blob_service_client.get_container_client(container_name)
blobs = list(container_client.list_blobs())

print(f"Blobs encontrados em '{container_name}': {[blob.name for blob in blobs]}")


