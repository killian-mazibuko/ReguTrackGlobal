import streamlit as st
from test_rag import run_test

st.set_page_config(page_title="ReguTrack Global", layout="wide")

st.title("ReguTrack Global: Compliance AI")
st.sidebar.info("Currently monitoring: South Africa, Nigeria, Kenya, UK, US")

query = st.chat_input("Ex: What are the 2026 South Africa requirements for data protection?")

if query:
    with st.spinner("Analyzing jurisdiction..."):
        # Your run_test should now return (answer, index_name, sources)
        answer, index, sources = run_test(query) 
        
    st.markdown(f"**Selected Index:** `{index}`")
    st.write(answer)
    
    with st.expander("View Legal Sources"):
        for src in sources:
            st.caption(f"📄 Source: {src['file']}")