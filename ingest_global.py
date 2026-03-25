import os
import json
import requests
import base64
import time
from azure.core.exceptions import ServiceResponseError
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from azure.search.documents import SearchClient

# 1. Initialize the token provider
# This replaces the need for an API Key
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

# --- CONFIGURATION ---
DI_ENDPOINT = "https://cog-di-hks3xzhnncdl4.cognitiveservices.azure.com/"
SEARCH_SERVICE_NAME = "gptkb-hks3xzhnncdl4"
API_VERSION = "2024-07-01"
PDF_FOLDER = "./data/pdfs"
TARGET_INDEX = "idx-regutrack-global"

# OpenAI Config for Embeddings (Required for Vector Search)
OPENAI_ENDPOINT = "https://cog-hks3xzhnncdl4.openai.azure.com/"
OPENAI_DEPLOYMENT = "text-embedding-3-large" # Deployment name for embeddings

# Initialize Clients
credential = DefaultAzureCredential()
di_client = DocumentIntelligenceClient(DI_ENDPOINT, credential)
oa_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT, 
    azure_ad_token_provider=token_provider, # Use API Key or Token
    api_key=None, # Set to None since we're using token provider 
    api_version="2023-05-15"
)

def get_embedding(text):
    """Generates a vector embedding for the chunk to enable Semantic Search."""
    text = text.replace("\n", " ")
    return oa_client.embeddings.create(input=[text], model=OPENAI_DEPLOYMENT, dimensions=1536).data[0].embedding

def extract_pdf_content_base64(file_path):
    print(f"--- Processing: {os.path.basename(file_path)} ---")
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        poller = di_client.begin_analyze_document(
            model_id="prebuilt-layout",
            body={"base64Source": base64_pdf},
            output_content_format="markdown",
        )
        return poller.result().content
    except Exception as e:
        print(f"Extraction failed: {e}")
        return None

# Initialize the Search Client once at the top
search_client = SearchClient(
    endpoint=f"https://{SEARCH_SERVICE_NAME}.search.windows.net",
    index_name=TARGET_INDEX,
    credential=DefaultAzureCredential() # This uses your 'az login' identity
)

def upload_to_search(document_data):
    """Uploads using the secure SDK instead of raw REST calls."""
    try:
        search_client.upload_documents(documents=[document_data])
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False

if __name__ == "__main__":
    with open('metadata.json', 'r') as f:
        master_metadata = json.load(f)
    counter = 0
    for doc in master_metadata:
        counter += 1
        if counter < 13: continue
        pdf_path = os.path.join(PDF_FOLDER, doc['file_name'])
        
        if os.path.exists(pdf_path):
            full_text = extract_pdf_content_base64(pdf_path)
            
            if full_text:
                # 4000 char chunks for legal context retention
                chunks = [full_text[i:i+4000] for i in range(0, len(full_text), 4000)]
                print(f"Uploading {len(chunks)} chunks to {TARGET_INDEX}...")
                
                for i, chunk in enumerate(chunks):
                    # Step 1: Generate Embedding for this chunk
                    vector = get_embedding(chunk)
                    
                    # Step 2: Map to the Template Schema
                    search_doc = {
                        "id": f"{doc['id']}_{i}".replace("-", "_"),
                        "content": chunk,              # Text content
                        "embedding": vector,           # Vector data
                        "filepath": doc['file_name'],  # REQUIRED for citations
                        "jurisdiction": doc['jurisdiction'],
                        "category": doc['category']
                    }
                    
                    success = upload_to_search(search_doc)
                    if not success:
                        print(f"Failed chunk {i}")
            
            time.sleep(2) # Avoid rate limits
        else:
            print(f"Missing file: {doc['file_name']}")

    print("\n--- Project Milestone: Unified Governed Index Complete ---")