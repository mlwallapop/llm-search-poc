# LLM-Powered Search PoC

This repository contains a proof-of-concept (PoC) application that demonstrates how to use a Large Language Model (LLM) to improve search relevance and re-rank search results. The project supports both manual query analysis and bulk analysis from a CSV file. It also includes a settings panel where you can configure the prompt templates and LLM parameters (provider, model, temperature).

Repository: https://github.com/mlwallapop/llm-search-poc

## Functionalities

- **Manual Query Analysis:**  
  Type a query (e.g., "silla de madera para mesa de exterior") and retrieve search results from the Wallapop API.  
  The app shows three views:
  - **Baseline:** The original order from the search engine.
  - **LLM Listwise Ranking:** Re-ranks results using a listwise approach with detailed reasoning.
  - **LLM Pointwise Ranking:** Re-ranks results using individual scores for each result.

- **CSV Bulk Analysis:**  
  Upload a CSV file containing search keywords and associated metrics.  
  All numeric columns are automatically detected and range sliders are displayed (grouped four per row) in an "Advanced Filters" panel.  
  Once you’re happy with the filtered data, click the "Process Bulk" button to analyze each keyword from the filtered CSV. Each keyword’s analysis is displayed in a collapsible panel with sub-tabs for Baseline, Listwise, and Pointwise ranking.

- **Settings:**  
  Under the Settings tab you can:
  - Configure the prompt templates used for pointwise and listwise ranking.
  - Select the LLM provider. Only providers with corresponding API keys set in your environment (e.g., OpenAI, Gemini, or Bedrock) are shown.
  - Choose an appropriate model and adjust the temperature.
  
  Changes are saved to the configuration and immediately affect how the ranking functions generate prompts.

## Setup and Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/mlwallapop/llm-search-poc.git
cd llm-search-poc
```

2. **Create a Virtual Environment and Install Dependencies: ONLY IF USING LOCAL ENVIRONMENT**

```bash
python3.11 -m venv venv
source venv/bin/activate        # On Windows use: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Set Up Environment Variables:**

Copy the provided env.dist file to .env and update with your API keys:

```bash
cp env.dist .env
```

Edit the .env file and fill in your:
- OPENAI_API_KEY
- GEMINI_API_KEY
- BEDROCK_API_KEY

## Running the Project

### Running with Docker Compose (for development)

A Docker Compose configuration is provided to support hot reload during development.

1. **Build and Run:**

```bash
docker-compose up --build
```

Your app will be accessible at [http://localhost:7777](http://localhost:7777).

### Running Locally

To run the application locally, execute:

```bash
streamlit run app/streamlit_app.py
```

The app will launch in your browser using a full-screen wide layout. It provides top-level tabs for Manual Query, CSV Bulk Analysis, and Settings.

## Explanation of Settings

- **Prompt Templates:**  
  In the Settings tab you can edit:
  - **Pointwise Prompt Template:** Used to score individual query-document pairs.
  - **Listwise Prompt Template:** Used to rank a set of search results along with detailed reasoning and query interpretation.
  
- **LLM Settings:**  
  In the Settings tab you can configure:
  - **LLM Provider:** The available providers are shown based on which API keys are set in your environment. Options include ChatOpenAI, ChatGemini, and ChatBedrock.
  - **LLM Model:** Choose from models appropriate for the selected provider (e.g., "gpt-4o-mini" for ChatOpenAI, "gemini-1.5-pro" for ChatGemini, "llama3.3:latest" for ChatBedrock).
  - **LLM Temperature:** Adjusts the randomness of the responses (from 0 to 1).

When you click "Save Settings," your selections update the configuration used by the ranking functions.

## Project Structure

- **app/**: Contains the Streamlit application (streamlit_app.py).
- **src/**: Contains the core logic:
  - **search_engine.py:** Code to query the Wallapop API.
  - **ranking.py:** Functions to compute LLM-based scores and rankings.
  - **schemas.py:** Pydantic models for structured LLM responses.
  - **metrics.py:** Metric functions (e.g., NDCG calculation).
  - **config.py:** Default configuration for prompt templates and LLM settings.
- **.env:** Environment variables file (copy from env.dist).
- **docker-compose.yml & Dockerfile:** For running the app in a container with hot reload during development.
- **requirements.txt:** Python dependencies list.

## Additional Notes

- This project is a proof-of-concept designed for demonstration and learning purposes.
- The UI is organized into top-level tabs to separate Manual Query, CSV Bulk Analysis, and Settings.
- For CSV Bulk Analysis, each keyword’s analysis appears in a collapsible panel with sub-tabs to keep the interface clean.
- Enjoy exploring and tweaking the LLM-Powered Search PoC!
