import math

def calculate_ndcg(scores):
    """
    Calculate the Normalized Discounted Cumulative Gain (NDCG) for a list of relevance scores.
    DCG is calculated as: sum((2^score - 1) / log2(i + 2)) for each score.
    IDCG is the DCG of the ideal (sorted) order.
    Returns the NDCG value.
    """
    def dcg(relevances):
        return sum((2 ** rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances))
    
    dcg_val = dcg(scores)
    ideal_scores = sorted(scores, reverse=True)
    idcg_val = dcg(ideal_scores)
    return dcg_val / idcg_val if idcg_val > 0 else 0
