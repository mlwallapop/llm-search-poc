# LLM-Powered Search PoC

LLM Search PoC is a hands-on project that demonstrates how to build and orchestrate applications powered by large language models (LLMs). The project contains various notebooks and code examples that illustrate different aspects of LLM integration, customization, and search functionalities. As the project evolves, more notebooks will be added to showcase new ideas and experiments.

## Project Structure

The project is organized into clear sections with dedicated notebooks for:
- LLM orchestration and integration
- Prompt engineering and templating
- Data connections and memory management
- Example applications and proof-of-concept demonstrations

Feel free to explore the folders and notebooks to see how each component of an LLM-powered application comes together!

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mlwallapop/llm-search-poc-main.git
   cd llm-search-poc-main
   ```

2. **Configure Environment Variable**

   **Important:** Append your name at the end of the `LANGSMITH_PROJECT` environment variable. For example:

   ```bash
   export LANGSMITH_PROJECT=llm-search-poc-yourname
   ```

3. **Build and Run the Containers**

   Use Docker Compose to build and run the project in detached mode:

   ```bash
   docker-compose up -d
   ```

   This command will start all the necessary services for the project.

## Notebook folder

In the notebook folder contains examples and proof-of-concepts projects that:
- **Demonstrates LLM Integration:** Shows how to leverage LLMs for search and other advanced applications.
- **Highlights Orchestration Techniques:** Provides examples of how to connect different modules such as prompt templates, data connections, and memory management.
- **Provides a Docker-Based Setup:** Offers a reproducible environment to experiment with and extend the application.

Enjoy exploring the project and feel free to add your own notebooks and experiments as the project grows!


## Streamlit Application

The streamlit application is a proof-of-concept (PoC) that demonstrates how to use a Large Language Model (LLM) to improve search relevance and re-rank search results. The project supports both manual query analysis and bulk analysis from a CSV file. It also includes a settings panel where you can configure the prompt templates and LLM parameters (provider, model, temperature).


### Functionalities

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

Your app will be accessible at [http://localhost:7777](http://localhost:7777).


#### Explanation of Settings

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

#### Project Structure

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

## Contributions

Contributions are welcome! If you have ideas for new notebooks, improvements, or additional integrations, please open an issue or submit a pull request.

Happy coding and exploring the world of LLM-powered applications!
