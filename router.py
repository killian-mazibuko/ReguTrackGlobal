import json
from openai import AzureOpenAI # Or your Gemini client
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Configuration for your LLM
endpoint = "https://cog-hks3xzhnncdl4.openai.azure.com/"
deployment = "gpt-4.1-mini" # or your deployment name

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(azure_endpoint=endpoint, azure_ad_token_provider=token_provider, api_version="2024-02-15-preview")

def get_routing_intent(user_query):
    """Asks the LLM to pick the right Jurisdiction and Category."""
    prompt = f"""
    Analyze the user query and return ONLY a JSON object with 'country' and 'topic'.
    Countries: SA, NG, KE, UK, US. 
    Topics: Finance, Digital.
    
    Query: "{user_query}"
    Response Format: {{"country": "SA", "topic": "Finance"}}
    """
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "system", "content": "You are a routing assistant."},
                  {"role": "user", "content": prompt}]
    )
    
    intent = json.loads(response.choices[0].message.content)
    # Map intent to your actual index names
    index_name = f"idx-{intent['country'].lower()}-{intent['topic'].lower()}"
    return index_name