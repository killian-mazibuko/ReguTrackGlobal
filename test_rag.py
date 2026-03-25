from router import get_routing_intent, client, deployment
from search_service import ReguSearch # The class we built in the previous step

# Initialize Search Service
SEARCH_ENDPOINT = "https://gptkb-hks3xzhnncdl4.search.windows.net"
searcher = ReguSearch(SEARCH_ENDPOINT)

# test_rag.py

def run_test(query):
    print(f"\n[1] User Query: {query}")
    
    # 1. ROUTE
    target_index = get_routing_intent(query)
    
    # 2. RETRIEVE
    context_chunks = searcher.search_jurisdiction(target_index, query)
    
    # FIX: Safety check for the 'content' key
    extracted_texts = []
    for c in context_chunks:
        # If 'content' is missing, it might be 'text' or another field
        # This line prevents the KeyError
        text = c.get('content') or c.get('text') or "No content found"
        extracted_texts.append(text)
    
    context_text = "\n".join(extracted_texts)
    
    # 3. GENERATE
    final_prompt = f"Use these legal excerpts to answer: {query}\n\nExcerpts:\n{context_text}"
    
    # Ensure you return all 3 values for app.py
    answer_obj = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    answer = answer_obj.choices[0].message.content
    return answer, target_index, context_chunks

# RUN THE TEST
if __name__ == "__main__":
    # Test a specific jurisdiction
    run_test("What are the capital requirements for banks in South Africa?")