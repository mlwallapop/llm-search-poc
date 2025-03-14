# src/config.py

# Default prompt template for pointwise scoring.
DEFAULT_POINTWISE_PROMPT = (
    "Given the following query and document, rate the semantic relevance on a scale of 1 to 10 and return only the numeric score.\n\n"
    "Query: \"{query}\"\n\nDocument: \"{document}\"\n\nScore:"
)

# Default prompt template for listwise ranking.
DEFAULT_LISTWISE_PROMPT = (
    "Rank the following search results for the query: '{query}' from most to least relevant. "
    "For each result, provide an object with 'index' (the original position, starting at 1), "
    "'score' (a relevance score between 1 and 10), and 'reasoning' (a brief explanation). "
    "Also include a property 'query_intent' that describes how you interpreted the query. "
    "Return the result as a JSON object with keys 'query_intent' and 'ranking'.\n\n"
    "{results_block}"
)
