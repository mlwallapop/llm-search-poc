from typing import List
from pydantic import BaseModel

class LLMPointwiseResponse(BaseModel):
    score: float

class LLMListwiseDetailedItem(BaseModel):
    index: int      # Original position (1-indexed)
    score: float    # Relevance score (1-10)
    reasoning: str  # Explanation for the score

class LLMListwiseDetailedResponse(BaseModel):
    query_intent: str                 # How the model interpreted the query
    ranking: List[LLMListwiseDetailedItem]  # Ranked list of items
