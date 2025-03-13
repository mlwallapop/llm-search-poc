# LLM-Powered Search PoC

This project demonstrates how to integrate an LLM (Large Language Model) as a judge to improve and measure semantic relevance for search results. The PoC uses the Wallapop API to fetch search results and then processes these results (e.g., extracting titles and descriptions). Later phases can integrate an LLM to re-rank and evaluate relevance.

## Features
- Query a live search API (Wallapop)
- Extract and display key fields (title, description)
- Modular code structure for further evaluation using LLMs
- Metrics calculation (e.g., NDCG) can be added in `evaluate_relevance.py`

## Getting Started

### Prerequisites
- Python 3.11
- pip
- [uv](https://pypi.org/project/uv/) if not installed, run: 
```bash
pip install uv
```

### Installation

1. **Clone the repository:**
```bash
git clone https://your-repo-url.git
cd llm_search_poc
```

2. **Create a virtual environment using Python 3.11:**
```bash
python3.11 -m venv venv
```

3. **Activate the virtual environment:**
- **On macOS/Linux:**
```bash
source venv/bin/activate
```
- **On Windows:**
```bash
venv\Scripts\activate
```

4. **Install dependencies using uv:**
```bash
uv sync -r requirements.txt
```

## Running the PoC

Run the main script:
```bash
python src/main.py
```

## Project Structure
- **src/**: Contains the Python modules:
  - `search_engine.py`: Module to query the Wallapop API.
  - `evaluate_relevance.py`: Placeholder module to integrate LLM judgment and calculate metrics.
  - `main.py`: Entry point for running the PoC.
- **docs/**: Contains design and architecture documents.
- **requirements.txt**: List of project dependencies.
- **.gitignore**: Files and directories to be ignored by Git.

## Future Work
- Integrate an LLM for re-ranking search results.
- Add evaluation metrics (e.g., NDCG, Precision, Recall).
- Expand the PoC to include user feedback and iterative improvements.
