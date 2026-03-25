import requests
# --- CONFIGURATION ---
SEARCH_SERVICE_NAME = "gptkb-hks3xzhnncdl4"
ADMIN_KEY = "BzDV4mA6Gq5kXdXY2IZ8VyNRae2NOw5jV8eB9VTb6nAzSeBv8C1Y"
API_VERSION = "2024-07-01"


index_names = [
    "idx-sa-finance", "idx-sa-digital", "idx-ng-finance", "idx-ng-digital",
    "idx-ke-finance", "idx-ke-digital", "idx-uk-finance", "idx-uk-digital",
    "idx-us-finance", "idx-us-digital"
]

for name in index_names:
    url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{name}?api-version={API_VERSION}"
    response = requests.delete(url, headers={'api-key': ADMIN_KEY})
    print(f"Deleted {name}: {response.status_code}")