from langchain_ollama import OllamaLLM
# Initialize the Ollama LLM with the desired model (e.g., "llama3")
llm = OllamaLLM(model="llama3.2:latest", temperature=0.2)

def get_relevance_score(query: str, document: str) -> float:
    """
    Uses the LLM to rate the relevance of a document given a query.
    The prompt instructs the LLM to return a numeric score between 1 and 10.
    """
    prompt = (
        f"Given the following query and document, "
        f"rate the semantic relevance on a scale of 1 to 10 and return only the numeric score.\n\n"
        f"Query: \"{query}\"\n\nDocument: \"{document}\"\n\nScore:"
    )
    response = llm(prompt)
    try:
        # Attempt to extract the first number in the response
        score = float(response.strip().split()[0])
    except Exception as e:
        print(f"Error parsing LLM response: {response}. Error: {e}")
        score = 0.0
    return score

def calculate_ndcg(scores):
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) for a list of scores.
    This is a simplified placeholder implementation.
    """
    return sum(scores) / len(scores) if scores else 0

def evaluate_results(query: str, results):
    """
    Iterate over search results and call the LLM for each query-document pair.
    Returns the aggregated NDCG metric and a list of individual scores.
    """
    scores = []
    for item in results:
        # Combine title and description for context
        document = f"{item.get('title', '')} {item.get('description', '')}"
        score = get_relevance_score(query, document)
        scores.append(score)
    ndcg = calculate_ndcg(scores)
    return ndcg, scores

if __name__ == "__main__":
    # Dummy test (for local testing)
    dummy_query = "silla de madera para mesa de exterior"
    dummy_results = [
        {"title": "Example Result 1", "description": "This is a great outdoor wooden chair."},
        {"title": "Example Result 2", "description": "A chair suitable for outdoor dining."}
    ]
    ndcg, scores = evaluate_results(dummy_query, dummy_results)
    print("Calculated NDCG:", ndcg)
    print("Individual LLM Scores:", scores)
