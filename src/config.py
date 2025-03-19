# src/config.py

# Default prompt templates
DEFAULT_POINTWISE_PROMPT = (
    """You are an expert document relevance rater. Your task is to assess the relevance of a document to a given intent and assign a rating from the following scale: 2, 1, 0, or "unknown".

    Here are the rating guidelines:

    **Rating 2: Highly Relevant (Good Result)**

    * The document perfectly or exactly matches the intent.
    * The document fully encompasses the intent, including cases where the intent specifies a set of items (e.g., multiple Pokemon cards, various accessories, a collection of books or DVDs).

    **Rating 1: Somewhat Relevant (Partial Match)**

    * The document is related to the intent but does not fully satisfy it. Common scenarios include:
        * The document is an accessory of the intended item (e.g., car parts for a car model, phone covers for a phone model, console controllers or games instead of the console).
        * The document contains only a portion of the intended item (e.g., a phone with a charger, but the document only describes the phone).
        * The document is highly related but not an exact match (e.g., similar models like an iPhone 13 for an iPhone 12, but not unrelated items like an Xbox console for a PS4 console).

    **Rating 0: Completely Irrelevant**

    * The document is entirely unrelated to the intent.

    **Rating "unknown": Unclear Relevance**

    * The relevance of the document cannot be determined due to:
        * A missing or unclear intent.
        * Missing or unclear item attributes.
        * The rater's lack of confidence in assigning a rating.

    **Instructions:**

    1.  Carefully analyze the provided intent and the document.
    2.  Determine the degree to which the document satisfies the intent based on the rating guidelines.
    3.  Assign the appropriate rating (2, 1, 0, or "unknown").
    
    Query: \"{query}\"\n\nDocument: \"{document}\"\n\nScore:"""
)

DEFAULT_LISTWISE_PROMPT = (
    "Rank the following search results for the query: '{query}' from most to least relevant. "
    "For each result, provide an object with 'index' (the original position, starting at 1), "
    "'score' (a relevance score between 1 and 10), and 'reasoning' (a brief explanation). "
    "Also include a property 'query_intent' that describes how you interpreted the query. "
    "Return the result as a JSON object with keys 'query_intent' and 'ranking'.\n\n"
    "{results_block}"
)

# LLM configuration defaults
DEFAULT_LLM_PROVIDER = "ChatOpenAI"  # Options: "ChatOpenAI", "ChatGemini", "ChatBedrock"
DEFAULT_LLM_MODEL = "gpt-4o-mini"      # For ChatOpenAI; for ChatGemini, e.g., "gemini-model-1"; for ChatBedrock, e.g., "amazon.titan-text-express-v1"
DEFAULT_LLM_TEMPERATURE = 0.0

# Default number of concurrent processes for pointwise ranking
DEFAULT_CONCURRENT_PROCESSES = 5
