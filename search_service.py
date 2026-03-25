from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class ReguSearch:
    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = AzureKeyCredential(key)

    def search_jurisdiction(self, index_name, query):
        client = SearchClient(self.endpoint, index_name, self.key)
        # We use Semantic Search for higher legal accuracy
        results = client.search(
            search_text=query,
            query_type="semantic",
            semantic_configuration_name="default-config",
            top=3
        )
        return [{"text": r["content"], "file": r.get("source_file", "Unknown")} for r in results]