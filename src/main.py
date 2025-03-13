from search_engine import search_engine
from evaluate_relevance import evaluate_results

def main():
    query = "silla de madera para mesa de exterior"
    print(f"Searching for: {query}\n")
    
    results = search_engine(query)
    for idx, res in enumerate(results, start=1):
        print(f"Result {idx}:")
        print(" Title:", res["title"])
        print(" Description:", res["description"])
        print("----------")
    
    # Placeholder: simulate LLM scores (in a real scenario, you'd call your LLM here)
    dummy_llm_scores = [8 for _ in results]
    ndcg = evaluate_results(results, dummy_llm_scores)
    print(f"\nCalculated NDCG (dummy values): {ndcg}")

if __name__ == "__main__":
    main()
