# Design Document for LLM-Powered Search PoC

## Overview
The objective of this project is to integrate an LLM as a judge to improve search relevance. The PoC consists of two main components:
1. **Search Engine Module:** Uses the Wallapop API to fetch search results.
2. **Evaluation Module:** Will integrate an LLM to assign relevance scores and compute metrics like NDCG.

## Architecture
- **Source Code (src/):** Contains modular Python scripts.
  - `search_engine.py`: Handles API requests and extracts key fields.
  - `evaluate_relevance.py`: Contains functions to calculate relevance metrics.
  - `main.py`: Entry point to run the PoC and demonstrate functionality.
- **Documentation (docs/):** Contains design and planning documents.
- **Dependencies:** Listed in `requirements.txt`. Key libraries include `requests`.

## Future Enhancements
- Integration with an LLM API for automated judgment.
- More advanced metric calculations.
- Dashboard for real-time metric monitoring.

## Workflow
1. The user submits a query.
2. The search engine module queries the Wallapop API.
3. Results are extracted and displayed.
4. (Future) The evaluation module calls an LLM to score each result.
5. Metrics are calculated and visualized.
