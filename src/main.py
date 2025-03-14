import streamlit as st
import pandas as pd
import copy
from search_engine import search_engine
from evaluate_relevance import get_relevance_score, listwise_rank, evaluate_results

st.set_page_config(layout="wide")

def re_rank_results(query: str, results):
    """
    Re-ranks the search results based on LLM relevance scores using a pointwise approach.
    Each result is annotated with an individual LLM score, and then the list is sorted
    in descending order of those scores.
    """
    for item in results:
        document = f"{item.get('title', '')} {item.get('description', '')}"
        item['llm_score'] = get_relevance_score(query, document)
    sorted_results = sorted(results, key=lambda x: x['llm_score'], reverse=True)
    return sorted_results

def main():
    st.title("LLM-Powered Search PoC (No Horizontal Scroll)")

    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior")

    if st.button("Search"):
        # 1. Baseline results
        results = search_engine(query)

        # Build a DataFrame for baseline
        baseline_df = pd.DataFrame({
            "Title": [r["title"] for r in results],
        })

        # 2. LLM Listwise Ranking
        #    This returns a tuple: (sorted_list, query_intent)
        #    where each item in sorted_list has 'llm_score' and 'llm_reasoning'
        listwise_results, query_intent = listwise_rank(query, copy.deepcopy(results))
        listwise_df = pd.DataFrame({
            "Title": [r["title"] for r in listwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in listwise_results],
            "Reasoning": [r.get("llm_reasoning", "N/A") for r in listwise_results],
        })

        # 3. LLM Pointwise Ranking
        pointwise_results = re_rank_results(query, copy.deepcopy(results))
        pointwise_df = pd.DataFrame({
            "Title": [r["title"] for r in pointwise_results],
            "LLM Score": [r.get("llm_score", "N/A") for r in pointwise_results],
        })

        # Display each ranking in its own tab
        tab1, tab2, tab3 = st.tabs(["Baseline", "LLM Listwise", "LLM Pointwise"])

        with tab1:
            st.subheader("Baseline Results")
            st.dataframe(baseline_df, use_container_width=True)

        with tab2:
            st.subheader("LLM Listwise Ranking")
            st.markdown(f"**Model interpreted query as**: {query_intent}")
            st.dataframe(listwise_df, use_container_width=True)

        with tab3:
            st.subheader("LLM Pointwise Ranking")
            st.dataframe(pointwise_df, use_container_width=True)

if __name__ == "__main__":
    main()
