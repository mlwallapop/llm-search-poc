import os
import sys
import streamlit as st
import pandas as pd
import copy

# Add project root to sys.path so that "src" can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.search_engine import search_engine
from src.ranking import get_relevance_score, listwise_rank, re_rank_results

st.set_page_config(layout="wide", page_title="LLM-Powered Search PoC")

def run_manual_query():
    st.header("Manual Query Analysis")
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior", key="manual_query")
    
    if st.button("Search (Manual)", key="manual_search"):
        # Fetch baseline results
        results = search_engine(query)
        for i, r in enumerate(results):
            r["original_index"] = i + 1
        
        # Build Baseline DataFrame
        baseline_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in results],
            "Title": [r["title"] for r in results]
        })
        
        # Obtain listwise ranking
        listwise_results, query_intent = listwise_rank(query, copy.deepcopy(results))
        listwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in listwise_results],
            "Title": [r["title"] for r in listwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in listwise_results],
            "Reasoning": [r.get("llm_reasoning", "N/A") for r in listwise_results]
        })
        
        # Obtain pointwise ranking
        pointwise_results = re_rank_results(query, copy.deepcopy(results))
        pointwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in pointwise_results],
            "Title": [r["title"] for r in pointwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in pointwise_results]
        })
        
        # Create sub-tabs for analysis
        m_tab1, m_tab2, m_tab3 = st.tabs(["Baseline", "LLM Listwise", "LLM Pointwise"])
        with m_tab1:
            st.subheader("Baseline Results")
            st.dataframe(baseline_df, use_container_width=True)
        with m_tab2:
            st.subheader("LLM Listwise Ranking")
            st.markdown(f"**Model interpreted query as:** {query_intent}")
            st.dataframe(listwise_df, use_container_width=True)
        with m_tab3:
            st.subheader("LLM Pointwise Ranking")
            st.dataframe(pointwise_df, use_container_width=True)

def run_csv_bulk():
    st.header("CSV Bulk Analysis")
    st.write("Upload a CSV file with search keywords and additional metrics.")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="bulk_csv")
    delimiter = st.selectbox("Select CSV delimiter:", [",", "\t", ";", "|"], index=0, key="csv_delimiter")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=delimiter)
        except Exception as e:
            st.error("Error reading CSV file. Please check the delimiter or file format.")
            st.stop()
        
        st.markdown("### Uploaded Data")
        st.dataframe(df, use_container_width=True)
        
        # Optional filters
        if "nb_searches" in df.columns:
            min_nb_searches = st.number_input("Minimum nb_searches", min_value=0, value=0, step=1, key="min_nb_searches")
            df = df[df["nb_searches"] >= min_nb_searches]
        else:
            st.warning("Column 'nb_searches' not found in CSV.")
        
        if "search_to_pi_by_search" in df.columns:
            col_min = float(df["search_to_pi_by_search"].min())
            col_max = float(df["search_to_pi_by_search"].max())
            search_to_pi_range = st.slider("Range for search_to_pi_by_search", min_value=col_min, max_value=col_max, value=(col_min, col_max), key="pi_range")
            df = df[(df["search_to_pi_by_search"] >= search_to_pi_range[0]) &
                    (df["search_to_pi_by_search"] <= search_to_pi_range[1])]
        else:
            st.warning("Column 'search_to_pi_by_search' not found in CSV.")
        
        st.markdown("### Filtered Data")
        st.dataframe(df, use_container_width=True)
        
        # For each keyword in the filtered CSV, process the analysis in an expander.
        st.markdown("## Bulk Analysis by Keyword")
        for idx, row in df.iterrows():
            keyword = row.get("search_keywords", None)
            if not keyword:
                continue
            with st.expander(f"Analysis for keyword: {keyword}"):
                # Run analysis for this keyword
                results = search_engine(keyword)
                for i, r in enumerate(results):
                    r["original_index"] = i + 1
                
                baseline_df = pd.DataFrame({
                    "Original Pos.": [r["original_index"] for r in results],
                    "Title": [r["title"] for r in results]
                })
                
                listwise_results, query_intent = listwise_rank(keyword, copy.deepcopy(results))
                listwise_df = pd.DataFrame({
                    "Original Pos.": [r["original_index"] for r in listwise_results],
                    "Title": [r["title"] for r in listwise_results],
                    "LLM Score": [r.get("llm_score", "N/A") for r in listwise_results],
                    "Reasoning": [r.get("llm_reasoning", "N/A") for r in listwise_results]
                })
                
                pointwise_results = re_rank_results(keyword, copy.deepcopy(results))
                pointwise_df = pd.DataFrame({
                    "Original Pos.": [r["original_index"] for r in pointwise_results],
                    "Title": [r["title"] for r in pointwise_results],
                    "LLM Score": [r.get("llm_score", "N/A") for r in pointwise_results]
                })
                
                # Use sub-tabs for each analysis type inside the expander
                b_tab, l_tab, p_tab = st.tabs(["Baseline", "LLM Listwise", "LLM Pointwise"])
                with b_tab:
                    st.subheader("Baseline")
                    st.dataframe(baseline_df, use_container_width=True)
                with l_tab:
                    st.subheader("LLM Listwise Ranking")
                    st.markdown(f"**Model interpreted query as:** {query_intent}")
                    st.dataframe(listwise_df, use_container_width=True)
                with p_tab:
                    st.subheader("LLM Pointwise Ranking")
                    st.dataframe(pointwise_df, use_container_width=True)

def main():
    st.title("LLM-Powered Search PoC")
    # Top-level mode selection using tabs
    top_tab1, top_tab2 = st.tabs(["Manual Query", "CSV Bulk Analysis"])
    
    with top_tab1:
        run_manual_query()
    
    with top_tab2:
        run_csv_bulk()

if __name__ == "__main__":
    main()
