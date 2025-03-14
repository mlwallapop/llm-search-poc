import streamlit as st
from search_engine import search_engine
from evaluate_relevance import get_relevance_score, listwise_rank

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
    st.title("LLM-Powered Search PoC")
    query = st.text_input("Enter search query:", "silla de madera para mesa de exterior")
    #results = search_engine(query)
    #print(listwise_rank(query, results))
    if st.button("Search"):
        # Fetch results from the search engine (baseline order)
        results = search_engine(query)
        
        st.subheader("Baseline Order")
        for idx, res in enumerate(results, start=1):
            st.write(f"{idx}. {res['title']}")
        
        # Get a listwise re-ranked order
        sorted_listwise = listwise_rank(query, results)
        st.subheader("LLM Re-ranked Order (Listwise)")
        for idx, res in enumerate(sorted_listwise, start=1):
            st.write(f"{idx}. {res['title']} (Score: {res.get('llm_score', 'N/A')})")
        
        # Also show pointwise re-ranking for comparison
        sorted_pointwise = re_rank_results(query, results)
        st.subheader("LLM Re-ranked Order (Pointwise)")
        for idx, res in enumerate(sorted_pointwise, start=1):
            st.write(f"{idx}. {res['title']} (Score: {res.get('llm_score', 'N/A')})")

if __name__ == "__main__":
    main()
