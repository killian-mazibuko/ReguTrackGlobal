
import requests

# --- CONFIGURATION ---
SEARCH_SERVICE_NAME = "gptkb-hks3xzhnncdl4"
ADMIN_KEY = "BzDV4mA6Gq5kXdXY2IZ8VyNRae2NOw5jV8eB9VTb6nAzSeBv8C1Y"
API_VERSION = "2024-07-01"

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

headers = {'Content-Type': 'application/json', 'api-key': ADMIN_KEY}

schema["name"] = index_name
requests.put(f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{index_name}?api-version={API_VERSION}", headers=headers, json=schema)
print(f"Created: {index_name}")