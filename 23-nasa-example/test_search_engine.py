from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

import os

load_dotenv()

index_name = "py-rag-tutorial-idx"

# Vector Search using text-to-vector conversion of the query string
query = "where is Tsauchab River located?"  

search_client = SearchClient(endpoint=os.environ['AZURE_SEARCH_SERVICE'], credential=DefaultAzureCredential(), index_name=index_name)
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")
  
docs = search_client.search(  
    search_text=query,  
    vector_queries=[vector_query],
    select=["chunk", "title", "locations"],
    top=1
)  
  
print(f"🔍 Query: {query}\n")

for i, doc in enumerate(docs, 1):
    print(f"📄 Result #{i}")
    print(f"🔹 Score: {doc.get('@search.score', 'N/A'):.4f}")
    print(f"🔹 Title: {doc.get('title', 'N/A')}")
    print(f"🔹 Locations: {doc.get('locations', [])}")
    print("📝 Chunk:")
    print(doc.get("chunk", "N/A"))
    print("-" * 60)