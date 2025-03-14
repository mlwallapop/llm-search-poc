import streamlit as st
import pandas as pd
from search_engine import search_engine
from evaluate_relevance import get_relevance_score, listwise_rank

st.set_page_config(layout="wide")

def main():
    st.title("LLM-Powered Search PoC")
    
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior")
    
    if st.button("Search"):
        # Fetch baseline results from the search engine
        results = search_engine(query)
        
        baseline_df = pd.DataFrame({
            "Title": [res["title"] for res in results]
        })
        
        # Obtain listwise re-ranked results (with additional score and reasoning)
        sorted_listwise, query_intent = listwise_rank(query, results)
        listwise_df = pd.DataFrame({
            "Title": [res["title"] for res in sorted_listwise],
            "LLM Score": [res.get("llm_score", "N/A") for res in sorted_listwise],
            "Reasoning": [res.get("llm_reasoning", "N/A") for res in sorted_listwise]
        })
        
        # Display baseline and listwise ranking in two columns (each occupying half width)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Baseline Order")
            st.dataframe(baseline_df, use_container_width=True)
        with col2:
            st.subheader("LLM Listwise Ranking")
            st.write("Model interpreted query as:", query_intent)
            st.dataframe(listwise_df, use_container_width=True)

if __name__ == "__main__":
    main()
