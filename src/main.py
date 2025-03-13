from search_engine import search_engine
from evaluate_relevance import evaluate_results

def main():
    query = "silla de madera para mesa de exterior"
    print(f"Searching for: {query}\n")
    
    # Fetch results from the search engine (Wallapop API)
    results = search_engine(query)
    for idx, res in enumerate(results, start=1):
        print(f"Result {idx}:")
        print(" Title:", res["title"])
        print(" Description:", res["description"])
        print("----------")
    
    # Evaluate the results using the LLM as a judge via LangChain Ollama
    ndcg, scores = evaluate_results(query, results)
    print(f"\nCalculated NDCG: {ndcg}")
    print("LLM Relevance Scores:", scores)

if __name__ == "__main__":
    main()
