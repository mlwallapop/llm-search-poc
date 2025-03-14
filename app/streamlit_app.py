import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
import copy
from src.search_engine import search_engine
from src.ranking import get_relevance_score, listwise_rank, re_rank_results

st.set_page_config(layout="wide")

def main():
    st.title("LLM-Powered Search PoC")
    
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior")
    
    if st.button("Search"):
        # Fetch baseline results from the search engine
        results = search_engine(query)
        
        # Annotate each result with its original position
        for i, r in enumerate(results):
            r["original_index"] = i + 1

        # Build DataFrame for baseline order
        baseline_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in results],
            "Title": [r["title"] for r in results]
        })
        
        # Obtain listwise re-ranked results (with LLM scores and reasoning)
        listwise_results, query_intent = listwise_rank(query, copy.deepcopy(results))
        listwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in listwise_results],
            "Title": [r["title"] for r in listwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in listwise_results],
            "Reasoning": [r.get("llm_reasoning", "N/A") for r in listwise_results]
        })
        
        # Obtain pointwise re-ranked results
        pointwise_results = re_rank_results(query, copy.deepcopy(results))
        pointwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in pointwise_results],
            "Title": [r["title"] for r in pointwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in pointwise_results]
        })
        
        # Display results in three tabs to avoid horizontal scrolling
        tab1, tab2, tab3 = st.tabs(["Baseline", "LLM Listwise", "LLM Pointwise"])
        with tab1:
            st.subheader("Baseline Results")
            st.dataframe(baseline_df, use_container_width=True)
        with tab2:
            st.subheader("LLM Listwise Ranking")
            st.markdown(f"**Model interpreted query as:** {query_intent}")
            st.dataframe(listwise_df, use_container_width=True)
        with tab3:
            st.subheader("LLM Pointwise Ranking")
            st.dataframe(pointwise_df, use_container_width=True)

if __name__ == "__main__":
    main()
