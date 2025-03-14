import os
import sys
import streamlit as st
import pandas as pd
import copy

# Add project root to sys.path so that "src" can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.search_engine import search_engine
from src.ranking import get_relevance_score, listwise_rank, re_rank_results
import src.config as config

st.set_page_config(layout="wide", page_title="LLM-Powered Search PoC")

def run_manual_query():
    st.header("Manual Query Analysis")
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior", key="manual_query")
    
    if st.button("Search (Manual)", key="manual_search"):
        results = search_engine(query)
        for i, r in enumerate(results):
            r["original_index"] = i + 1

        baseline_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in results],
            "Title": [r["title"] for r in results]
        })
        
        listwise_results, query_intent = listwise_rank(query, copy.deepcopy(results))
        listwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in listwise_results],
            "Title": [r["title"] for r in listwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in listwise_results],
            "Reasoning": [r.get("llm_reasoning", "N/A") for r in listwise_results]
        })
        
        pointwise_results = re_rank_results(query, copy.deepcopy(results))
        pointwise_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in pointwise_results],
            "Title": [r["title"] for r in pointwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in pointwise_results]
        })
        
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
    col_file, col_delim = st.columns(2)
    with col_file:
        uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], key="bulk_csv")
    with col_delim:
        delimiter = st.selectbox("Delimiter", [",", "\t", ";", "|"], index=0, key="csv_delimiter")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=delimiter)
        except Exception as e:
            st.error("Error reading CSV file. Please check the delimiter or file format.")
            st.stop()
        
        with st.expander("Advanced Filters"):
            filters = {}
            numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
            # Group filters in rows of 6 columns
            for i in range(0, len(numeric_columns), 6):
                cols = st.columns(6)
                for j, col in enumerate(numeric_columns[i:i+6]):
                    col_min = float(df[col].min())
                    col_max = float(df[col].max())
                    if col_min == col_max:
                        filters[col] = (col_min, col_max)
                        cols[j].info(f"'{col}' constant: {col_min}")
                    else:
                        filters[col] = cols[j].slider(
                            f"{col} range",
                            min_value=col_min,
                            max_value=col_max,
                            value=(col_min, col_max),
                            key=f"filter_{col}"
                        )
        
        filtered_df = df.copy()
        for col, (min_val, max_val) in filters.items():
            filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]
        
        st.markdown("### Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)
        
        if st.button("Process Bulk", key="process_bulk"):
            st.markdown("## Bulk Analysis by Keyword")
            for idx, row in filtered_df.iterrows():
                keyword = row.get("search_keywords", None)
                if not keyword:
                    continue
                with st.expander(f"Analysis for keyword: {keyword}"):
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

def run_settings():
    st.header("Settings")
    st.markdown("### Configure Prompt Templates for Ranking")
    new_pointwise = st.text_area("Pointwise Prompt Template", value=config.DEFAULT_POINTWISE_PROMPT, height=150)
    new_listwise = st.text_area("Listwise Prompt Template", value=config.DEFAULT_LISTWISE_PROMPT, height=150)
    if st.button("Save Settings", key="save_settings"):
        config.DEFAULT_POINTWISE_PROMPT = new_pointwise
        config.DEFAULT_LISTWISE_PROMPT = new_listwise
        st.success("Settings updated successfully!")

def main():
    st.title("LLM-Powered Search PoC")
    top_tab1, top_tab2, top_tab3 = st.tabs(["Manual Query", "CSV Bulk Analysis", "Settings"])
    
    with top_tab1:
        run_manual_query()
    with top_tab2:
        run_csv_bulk()
    with top_tab3:
        run_settings()

if __name__ == "__main__":
    main()
