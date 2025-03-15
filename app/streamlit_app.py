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
import folium
from streamlit_folium import st_folium

def run_manual_query():
    st.header("Manual Query Analysis")
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior", key="manual_query")
    
    # Default coordinates (e.g., Barcelona)
    default_lat = 41.387917
    default_lon = 2.1699187

    st.markdown("### Adjust Search Location")
    st.info("Drag the marker and then click on the map to update the coordinates.")

    # Create a folium map with a draggable marker
    m = folium.Map(location=[default_lat, default_lon], zoom_start=12)
    folium.Marker(
        location=[default_lat, default_lon],
        popup="Drag me!",
        draggable=True
    ).add_to(m)
    
    # Render the map and capture the state
    map_data = st_folium(m, width=700, height=450)
    
    # Extract updated coordinates:
    # (Note: st_folium returns 'last_clicked' when the map is clicked.
    # To update coordinates, drag the marker then click anywhere on the map.)
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
    else:
        lat = default_lat
        lon = default_lon

    st.write(f"Selected location: {lat}, {lon}")
    
    if st.button("Search (Manual)", key="manual_search"):
        results = search_engine(query, latitude=lat, longitude=lon)
        for i, r in enumerate(results):
            r["original_index"] = i + 1

        baseline_df = pd.DataFrame({
            "Original Pos.": [r["original_index"] for r in results],
            "Title": [r["title"] for r in results],
            "Description": [r["description"] for r in results]
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
            for i in range(0, len(numeric_columns), 4):
                cols = st.columns(4)
                for j, col in enumerate(numeric_columns[i:i+4]):
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
                    
                    # Baseline table now includes Description
                    baseline_df = pd.DataFrame({
                        "Original Pos.": [r["original_index"] for r in results],
                        "Title": [r["title"] for r in results],
                        "Description": [r["description"] for r in results]
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
    
    st.markdown("### Configure LLM Settings")
    provider_options = []
    if os.getenv("OPENAI_API_KEY"):
        provider_options.append("ChatOpenAI")
    if os.getenv("GEMINI_API_KEY"):
        provider_options.append("ChatGemini")
    if os.getenv("BEDROCK_API_KEY"):
        provider_options.append("ChatBedrock")
    if not provider_options:
        provider_options.append("ChatOpenAI")
        st.warning("No API keys found; defaulting to ChatOpenAI provider.")
    new_provider = st.selectbox("LLM Provider", options=provider_options, index=provider_options.index(config.DEFAULT_LLM_PROVIDER) if config.DEFAULT_LLM_PROVIDER in provider_options else 0)
    if new_provider == "ChatOpenAI":
        model_options = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]
    elif new_provider == "ChatGemini":
        model_options = ["gemini-model-1", "gemini-model-2"]
    elif new_provider == "ChatBedrock":
        model_options = ["amazon.titan-text-express-v1", "bedrock-model-2"]
    else:
        model_options = []
    new_model = st.selectbox("LLM Model", options=model_options, index=model_options.index(config.DEFAULT_LLM_MODEL) if config.DEFAULT_LLM_MODEL in model_options else 0)
    new_temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.0, value=config.DEFAULT_LLM_TEMPERATURE, step=0.1)
    
    st.markdown("### Configure Concurrency Settings")
    new_concurrency = st.number_input("Concurrent Processes", min_value=1, max_value=20, value=config.DEFAULT_CONCURRENT_PROCESSES, step=1)
    
    if st.button("Save Settings", key="save_settings"):
        config.DEFAULT_POINTWISE_PROMPT = new_pointwise
        config.DEFAULT_LISTWISE_PROMPT = new_listwise
        config.DEFAULT_LLM_PROVIDER = new_provider
        config.DEFAULT_LLM_MODEL = new_model
        config.DEFAULT_LLM_TEMPERATURE = new_temperature
        config.DEFAULT_CONCURRENT_PROCESSES = new_concurrency
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
