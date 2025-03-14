import math
import re
from typing import List, Tuple
from langchain_openai import ChatOpenAI
from src.schemas import LLMPointwiseResponse, LLMListwiseDetailedResponse
from src.metrics import calculate_ndcg
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM (adjust parameters as needed)
llm = ChatOpenAI()

def get_relevance_score(query: str, document: str) -> float:
    """
    Uses the LLM to rate the relevance of a document given a query.
    Returns a float score extracted from the LLM's structured output.
    """
    prompt = (
        f"Given the following query and document, "
        f"rate the semantic relevance on a scale of 1 to 10 and return only the numeric score.\n\n"
        f"Query: \"{query}\"\n\nDocument: \"{document}\"\n\nScore:"
    )
    response = llm.with_structured_output(LLMPointwiseResponse).invoke(prompt)
    return response.score

def re_rank_results(query: str, results: List[dict]) -> List[dict]:
    """
    Re-ranks the search results based on LLM relevance scores using a pointwise approach.
    Each result is annotated with its LLM score and then the list is sorted in descending order.
    """
    for item in results:
        document = f"{item.get('title', '')} {item.get('description', '')}"
        item['llm_score'] = get_relevance_score(query, document)
    sorted_results = sorted(results, key=lambda x: x['llm_score'], reverse=True)
    return sorted_results

def evaluate_results(query: str, results: List[dict]) -> Tuple[float, List[float]]:
    """
    Iterates over search results, obtains pointwise LLM scores for each, and calculates NDCG.
    Returns a tuple (ndcg, scores).
    """
    scores = []
    for item in results:
        document = f"{item.get('title', '')} {item.get('description', '')}"
        score = get_relevance_score(query, document)
        scores.append(score)
    ndcg = calculate_ndcg(scores)
    return ndcg, scores

def listwise_rank(query: str, results: List[dict]) -> Tuple[List[dict], str]:
    """
    Builds a prompt with all search results (titles and descriptions) and asks the LLM to rank them.
    The LLM returns a JSON object with:
      - 'query_intent': a string describing how it interpreted the query.
      - 'ranking': a list of objects (each with 'index', 'score', and 'reasoning').
    This function reorders the results based on the ranking and attaches each item's score and reasoning.
    Returns a tuple (sorted_results, query_intent).
    """
    prompt = (
        f"Rank the following search results for the query: '{query}' from most to least relevant. "
        "For each result, provide an object with 'index' (the original position, starting at 1), "
        "'score' (a relevance score between 1 and 10), and 'reasoning' (a brief explanation). "
        "Also, include a property 'query_intent' that describes how you interpreted the query. "
        "Return the result as a JSON object with keys 'query_intent' and 'ranking'.\n\n"
    )
    for idx, item in enumerate(results, start=1):
        title = item.get('title', '')
        description = item.get('description', '')
        prompt += f"{idx}. Title: {title}\n   Description: {description}\n\n"
    
    response = llm.with_structured_output(LLMListwiseDetailedResponse).invoke(prompt)
    new_ranking = response.ranking
    query_intent = response.query_intent
    
    sorted_results = []
    for ranking_item in new_ranking:
        if 1 <= ranking_item.index <= len(results):
            result = results[ranking_item.index - 1]
            result['llm_score'] = ranking_item.score
            result['llm_reasoning'] = ranking_item.reasoning
            sorted_results.append(result)
    return sorted_results, query_intent

if __name__ == "__main__":
    dummy_query = "silla de madera para mesa de exterior"
    dummy_results = [
        {"title": "Example Result 1", "description": "This is a great outdoor wooden chair."},
        {"title": "Example Result 2", "description": "A chair suitable for outdoor dining."}
    ]
    ndcg, scores = evaluate_results(dummy_query, dummy_results)
    print("Calculated NDCG:", ndcg)
    print("Individual LLM Scores:", scores)
    
    ranked_results, intent = listwise_rank(dummy_query, dummy_results)
    print("Model interpreted query as:", intent)
    for idx, res in enumerate(ranked_results, start=1):
        print(f"{idx}. {res['title']} (Score: {res.get('llm_score', 'N/A')}, Reasoning: {res.get('llm_reasoning', 'N/A')})")
