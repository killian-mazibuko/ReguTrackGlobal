
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex

# --- CONFIGURATION ---
SEARCH_SERVICE_NAME = "gptkb-hks3xzhnncdl4"

# Use role-based authentication
credential = DefaultAzureCredential()
endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"
client = SearchIndexClient(endpoint=endpoint, credential=credential)

# 1 indnex for all
index_name = "idx-regutrack-global"

schema = {
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
        {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True},
        # The template MANDATES this field for clickable citations
        {"name": "filepath", "type": "Edm.String", "searchable": True, "retrievable": True, "filterable": True},
        # Vector field for reduced hallucination (using text-embedding-3-small)
        {"name": "embedding", "type": "Collection(Edm.Single)", "searchable": True, "retrievable": True, "dimensions": 1536, "vectorSearchProfile": "HnswProfile"},
        {"name": "category", "type": "Edm.String", "filterable": True, "searchable": True},
        {"name": "jurisdiction", "type": "Edm.String", "filterable": True, "retrievable": True}
    ],
    "vectorSearch": {
        "algorithms": [{"name": "HnswAlgo", "kind": "hnsw"}],
        "profiles": [{"name": "HnswProfile", "algorithm": "HnswAlgo"}]
    },
    "semantic": {
        "configurations": [{
            "name": "default",
            "prioritizedFields": {
                "prioritizedContentFields": [{"fieldName": "content"}]
            }
        }]
    }
}

index = SearchIndex(name=index_name, fields=schema["fields"], vector_search=schema["vectorSearch"], semantic_search=schema["semantic"])
client.create_index(index)
print(f"Created: {index_name}")