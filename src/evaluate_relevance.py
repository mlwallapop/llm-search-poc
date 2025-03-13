import math
import re
from langchain_ollama import OllamaLLM

# Initialize the Ollama LLM with the desired model
llm = OllamaLLM(model="llama3.2:latest", temperature=0.2)

def get_relevance_score(query: str, document: str) -> float:
    """
    Uses the LLM to rate the relevance of a document given a query.
    The prompt instructs the LLM to return a numeric score between 1 and 10.
    
    To improve robustness:
      - The prompt clearly defines the expected output.
      - The function uses a regex to extract the first numeric value from the LLM response.
    """
    prompt = (
        f"Given the following query and document, "
        f"rate the semantic relevance on a scale of 1 to 10 and return only the numeric score.\n\n"
        f"Query: \"{query}\"\n\nDocument: \"{document}\"\n\nScore:"
    )
    
    response = llm(prompt)
    # Use regex to extract a number (integer or decimal) from the response
    match = re.search(r"(\d+(\.\d+)?)", response)
    if match:
        score = float(match.group(1))
    else:
        print(f"Error parsing LLM response: '{response}'. Defaulting score to 0.0")
        score = 0.0
    return score

def calculate_ndcg(scores):
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) for a list of relevance scores.
    
    DCG is computed as:
      DCG = sum[(2^relevance - 1) / log2(i+2)] for i in 0...n-1
      
    IDCG is the maximum possible DCG (i.e. scores sorted in descending order).
    
    NDCG = DCG / IDCG
    """
    def dcg(relevances):
        return sum((2 ** rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances))
    
    dcg_val = dcg(scores)
    # Sort scores in descending order to get the ideal ranking
    ideal_scores = sorted(scores, reverse=True)
    idcg_val = dcg(ideal_scores)
    return dcg_val / idcg_val if idcg_val > 0 else 0

def evaluate_results(query: str, results):
    """
    Iterates over search results and calls the LLM for each query-document pair.
    Returns:
      - The aggregated NDCG metric.
      - A list of individual LLM scores.
      
    It combines the title and description of each result to provide richer context.
    """
    scores = []
    for item in results:
        # Combine title and description for context
        document = f"{item.get('title', '')} {item.get('description', '')}"
        score = get_relevance_score(query, document)
        scores.append(score)
    ndcg = calculate_ndcg(scores)
    return ndcg, scores

def listwise_rank(query: str, results):
    """
    Creates a prompt that includes all search results (titles and descriptions)
    and asks the LLM to return a ranked list of items based on their relevance to the query.
    """
    # Build the list of results in the prompt
    prompt = f"Rank the following search results for the query: '{query}' from most to least relevant. Return only the ranking as a list of numbers corresponding to the original order (e.g., 2, 1, 3).\n\n"
    for idx, item in enumerate(results, start=1):
        title = item.get('title', '')
        description = item.get('description', '')
        prompt += f"{idx}. Title: {title}\n   Description: {description}\n\n"
    
    response = llm(prompt)  # Assuming llm is your LangChain LLM instance
    # Here, parse the response to get the new order. 
    # For example, if the response is "2, 1, 3", then:
    try:
        order = [int(num.strip()) for num in response.strip().split(',')]
    except Exception as e:
        print(f"Error parsing listwise ranking response: '{response}'. Error: {e}")
        order = list(range(1, len(results) + 1))
    
    # Reorder results based on the new ranking order
    sorted_results = [results[i-1] for i in order if 1 <= i <= len(results)]
    return sorted_results

if __name__ == "__main__":
    # Example test using dummy results
    dummy_query = "silla de madera para mesa de exterior"
    dummy_results = [
        {"title": "Example Result 1", "description": "This is a great outdoor wooden chair."},
        {"title": "Example Result 2", "description": "A chair suitable for outdoor dining."}
    ]
    ndcg, scores = evaluate_results(dummy_query, dummy_results)
    print("Calculated NDCG:", ndcg)
    print("Individual LLM Scores:", scores)
