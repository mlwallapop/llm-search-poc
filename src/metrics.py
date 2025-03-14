import math
from typing import List

def calculate_ndcg(scores: List[float]) -> float:
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) for a list of relevance scores.
    DCG = sum((2^score - 1) / log2(i + 2)) for each score.
    Returns the NDCG value.
    """
    def dcg(relevances: List[float]) -> float:
        return sum((2 ** rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances))
    
    dcg_val = dcg(scores)
    ideal_scores = sorted(scores, reverse=True)
    idcg_val = dcg(ideal_scores)
    return dcg_val / idcg_val if idcg_val > 0 else 0
