import math
import re
from typing import List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM (change to your desired model and parameters)
llm = ChatOpenAI()  # or use your Ollama setup if needed

# Existing pointwise response model
class LLMPointwiseResponse(BaseModel):
    score: float

# New detailed listwise models
class LLMListwiseDetailedItem(BaseModel):
    index: int      # original position (1-indexed)
    score: float    # relevance score between 1 and 10
    reasoning: str  # brief explanation behind the score

class LLMListwiseDetailedResponse(BaseModel):
    query_intent: str               # how the model understood the query
    ranking: List[LLMListwiseDetailedItem]  # list of ranked items

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
    
    response = llm.with_structured_output(LLMPointwiseResponse).invoke(prompt)
    return response.score

def calculate_ndcg(scores):
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) for a list of relevance scores.
    DCG = sum((2^relevance - 1) / log2(i+2)) for i in 0...n-1.
    IDCG is computed on the ideal (sorted) list.
    """
    def dcg(relevances):
        return sum((2 ** rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances))
    
    dcg_val = dcg(scores)
    ideal_scores = sorted(scores, reverse=True)
    idcg_val = dcg(ideal_scores)
    return dcg_val / idcg_val if idcg_val > 0 else 0

def evaluate_results(query: str, results):
    """
    Iterates over search results and calls the LLM for each query-document pair.
    Returns the aggregated NDCG metric and a list of individual LLM scores.
    """
    scores = []
    for item in results:
        document = f"{item.get('title', '')} {item.get('description', '')}"
        score = get_relevance_score(query, document)
        scores.append(score)
    ndcg = calculate_ndcg(scores)
    return ndcg, scores


def listwise_rank(query: str, results):
    """
    Creates a prompt that includes all search results (titles and descriptions)
    and asks the LLM to return a ranked list with each item's score and reasoning,
    as well as a property 'query_intent' that explains how the model interpreted the query.
    The expected output is a JSON object with two keys:
      - "query_intent": a string,
      - "ranking": a list of objects with "index", "score", and "reasoning".
    Returns a tuple: (sorted_results, query_intent)
    """
    prompt = (
        f"Rank the following search results for the query: '{query}' from most to least relevant. "
        "For each result, provide an object with 'index' (the original position, starting at 1), "
        "'score' (a relevance score between 1 and 10), and 'reasoning' (a brief explanation of why that score was given). "
        "Also, include a property 'query_intent' that describes how you interpreted the query. "
        "Return the result as a JSON object with keys 'query_intent' and 'ranking'.\n\n"
    )
    for idx, item in enumerate(results, start=1):
        title = item.get('title', '')
        description = item.get('description', '')
        prompt += f"{idx}. Title: {title}\n   Description: {description}\n\n"
    
    # Get the structured response using our detailed schema
    response = llm.with_structured_output(LLMListwiseDetailedResponse).invoke(prompt)
    
    new_ranking = response.ranking
    query_intent = response.query_intent
    
    sorted_results = []
    for ranking_item in new_ranking:
        if 1 <= ranking_item.index <= len(results):
            result = results[ranking_item.index - 1]
            # Attach the score and reasoning to each result
            result['llm_score'] = ranking_item.score
            result['llm_reasoning'] = ranking_item.reasoning
            sorted_results.append(result)
    return sorted_results, query_intent

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
    
    # Testing listwise ranking
    ranked_results = listwise_rank(dummy_query, dummy_results)
    for idx, res in enumerate(ranked_results, start=1):
        print(f"{idx}. {res['title']} (Score: {res.get('llm_score', 'N/A')})")
