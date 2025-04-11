from dotenv import load_dotenv
from azure.search.documents.indexes import SearchIndexerClient
from azure.identity import DefaultAzureCredential
import time
import os

load_dotenv()

# Inicializa o cliente
indexer_client = SearchIndexerClient(
    endpoint=os.environ["AZURE_SEARCH_SERVICE"],
    credential=DefaultAzureCredential()
)

# Nome do seu indexador
indexer_name = os.environ["INDEXER"]

# Pega o status atual do indexador
indexer_status = indexer_client.get_indexer_status(indexer_name)

while indexer_status.status == "running":
    print("Indexador ainda está em execução...")
    time.sleep(10)  # Espera 10 segundos antes de verificar novamente
    
    print(f"📌 Indexer status: {indexer_status.status}")
    print(f"📄 Documents processed: {indexer_status.last_result}")
    print()

    # Mostra erros, se houver
    if indexer_status.last_result != None and indexer_status.last_result.errors:
        print("🧨 Erros encontrados:")
        for err in indexer_status.last_result.errors:
            print(f"- Key: {err.key}")
            print(f"  Error Message: {err.error_message}")
            print()
    else:
        print("✅ Nenhum erro registrado.")

    indexer_status = indexer_client.get_indexer_status(indexer_name)

