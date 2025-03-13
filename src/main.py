from search_engine import search_engine
from evaluate_relevance import evaluate_results, get_relevance_score, listwise_rank

def re_rank_results(query: str, results):
    """
    Re-ranks the search results based on LLM relevance scores.
    Returns a new list of results sorted in descending order of the score.
    """
    # Annotate each result with its LLM score
    for item in results:
        document = f"{item.get('title', '')} {item.get('description', '')}"
        item['llm_score'] = get_relevance_score(query, document)
    # Sort results by the LLM score (highest first)
    sorted_results = sorted(results, key=lambda x: x['llm_score'], reverse=True)
    return sorted_results

def main():
    query = "silla de madera para mesa de exterior"
    print(f"Searching for: {query}\n")
    
    # Fetch results from the search engine (baseline order)
    results = search_engine(query)
    
    print("=== Baseline Order ===")
    for idx, res in enumerate(results, start=1):
        print(f"{idx}. {res['title']}")
    
    # Evaluate and re-rank the results using the LLM
    sorted_results = listwise_rank(query, results)
    
    print("\n=== LLM Re-ranked Order ===")
    for idx, res in enumerate(sorted_results, start=1):
        print(f"{idx}. {res['title']} (Score: {res.get('llm_score')})")
    
    # Optionally, compute aggregated metric (e.g. NDCG)
    #ndcg, scores = evaluate_results(query, results)
    #print(f"\nCalculated NDCG: {ndcg}")
    
if __name__ == "__main__":
    main()
