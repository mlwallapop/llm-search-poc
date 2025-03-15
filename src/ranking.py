import math
import re
from typing import List, Tuple, Dict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from src.schemas import LLMPointwiseResponse, LLMListwiseDetailedResponse
from src.metrics import calculate_ndcg
import src.config as config

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Instantiate the LLM based on the provider specified in config
if config.DEFAULT_LLM_PROVIDER == "ChatOpenAI":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=config.DEFAULT_LLM_MODEL, temperature=config.DEFAULT_LLM_TEMPERATURE)
elif config.DEFAULT_LLM_PROVIDER == "ChatGemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model=config.DEFAULT_LLM_MODEL, temperature=config.DEFAULT_LLM_TEMPERATURE)
elif config.DEFAULT_LLM_PROVIDER == "ChatBedrock":
    from langchain_aws import BedrockLLM
    llm = BedrockLLM(credentials_profile_name="bedrock-admin", model_id=config.DEFAULT_LLM_MODEL)
else:
    raise ValueError("Unsupported LLM provider: " + config.DEFAULT_LLM_PROVIDER)

def get_relevance_score(query: str, document: str) -> float:
    prompt = config.DEFAULT_POINTWISE_PROMPT.format(query=query, document=document)
    try:
        response = llm.with_structured_output(LLMPointwiseResponse).invoke(prompt)
        return response.score
    except Exception as e:
        logging.exception("LLM call failed in get_relevance_score")
        return 0.0

def re_rank_results(query: str, results: List[Dict]) -> List[Dict]:
    """
    Re-ranks search results using pointwise LLM relevance scores in parallel.
    Each result is processed concurrently using a thread pool (with a maximum number of workers
    defined in config.DEFAULT_CONCURRENT_PROCESSES). After all scores are computed, the results
    are sorted in descending order by the LLM score.
    """
    max_workers = config.DEFAULT_CONCURRENT_PROCESSES
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {
            executor.submit(get_relevance_score, query, f"{item.get('title','')} {item.get('description','')}"): item
            for item in results
        }
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                item['llm_score'] = future.result()
            except Exception as exc:
                logging.exception("Error computing score for item")
                item['llm_score'] = 0.0
    sorted_results = sorted(results, key=lambda x: x['llm_score'], reverse=True)
    return sorted_results

def evaluate_results(query: str, results: List[Dict]) -> Tuple[float, List[float]]:
    scores = []
    for item in results:
        document = f"{item.get('title','')} {item.get('description','')}"
        score = get_relevance_score(query, document)
        scores.append(score)
    ndcg = calculate_ndcg(scores)
    return ndcg, scores

def listwise_rank(query: str, results: List[Dict]) -> Tuple[List[Dict], str]:
    results_block = ""
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "")
        description = item.get("description", "")
        results_block += f"{idx}. Title: {title}\n   Description: {description}\n\n"
    prompt = config.DEFAULT_LISTWISE_PROMPT.format(query=query, results_block=results_block)
    try:
        response = llm.with_structured_output(LLMListwiseDetailedResponse).invoke(prompt)
    except Exception as e:
        logging.exception("LLM call failed in listwise_rank")
        return results, "No interpretation available."
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
        print(f"{idx}. {res['title']} (Score: {res.get('llm_score','N/A')}, Reasoning: {res.get('llm_reasoning','N/A')})")
