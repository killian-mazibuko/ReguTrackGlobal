import os
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

# --- CONFIGURATION ---
SEARCH_SERVICE_NAME = "gptkb-hks3xzhnncdl4"

# Use role-based authentication
credential = DefaultAzureCredential()
endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"
client = SearchIndexClient(endpoint=endpoint, credential=credential)

name="idx-regutrack-global"
try:
    client.delete_index(name)
    print(f"Deleted {name}: Success")
except Exception as e:
    print(f"Failed to delete {name}: {str(e)}")