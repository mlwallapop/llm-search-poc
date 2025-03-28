# 🚀 LLM-Powered Search and Orchestration Playground

👋 Welcome! This is your go-to playground to explore, experiment, and learn about orchestrating and integrating Large Language Models (LLMs) for search and enrichment applications. Dive in, discover, and create amazing LLM-powered experiences!

## 🌟 What Does This Project Offer?

- 📒 **Interactive Notebooks:** Explore retrieval augmented generation (RAG), embedding models, vector stores, prompt engineering, and more!
- 🎨 **Streamlit Application:** A hands-on demo app for LLM-based re-ranking of search results.
- 🌐 **Containerized LangGraph Server:** Run and manage advanced LLM orchestration through a dedicated LangGraph server.
- ⚙️ **Customizable Environment:** Easily configure your favorite LLM providers and settings.
- 🐳 **Docker-Based Setup:** Quick setup to jumpstart your experiments using Docker.

## 📂 Project Structure

- **app/**: Streamlit demo (`streamlit_app.py`).
- **src/**: Core utilities and logic.
- **notebooks/**: Interactive Jupyter notebooks covering exciting LLM topics.
- **langgraph/**: Advanced LLM orchestration and agent frameworks.
- **env.dist**: Template for environment variables (copy and customize to `.env`).
- **Dockerfile & docker-compose.yml**: Simple setup for reproducible development.

## 🛠️ Prerequisites

- 🐳 Docker and Docker Compose installed.
- 🐍 Python 3.11 recommended (if running locally without Docker).

## 🚦 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd llm-search-poc-main
```

### 2️⃣ Configure API Keys and Environment

Copy and set up your environment variables:

```bash
cp env.dist .env
```

Edit `.env` with your credentials:

```env
# LLM Providers
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional APIs
SERPAPI_API_KEY=your_serpapi_key
TAVILY_API_KEY=your_tavily_key

# LangSmith Tracing (optional)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=llm-playground-yourname
```

⚠️ **Important:** Personalize `LANGSMITH_PROJECT` to avoid conflicts!

### 3️⃣ Launch Your Playground

Build and start all services:

```bash
docker-compose up -d
```

🚀 Services running:

- 📚 **Jupyter Notebooks:** [http://localhost:8888](http://localhost:8888)
- 🎯 **Streamlit App (Search Re-ranking):** [http://localhost:7777](http://localhost:7777)
- 🌐 **LangGraph Server:** [http://localhost:2024](http://localhost:2024) (see below for usage details)

## 🎮 Using the Streamlit App

Experience LLM-enhanced search re-ranking with:

- **Manual Query Analysis:** Compare baseline results against LLM-ranked results.
- **CSV Bulk Analysis:** Process multiple queries from CSV files.
- **Settings Panel:** Fully customize prompts, providers, models, and temperature settings.

### ⚙️ Settings Explained

- ✍️ **Prompt Templates:** Customize prompts for various ranking methods.
- 🤖 **LLM Providers & Models:** Select your preferred provider and model (OpenAI, Gemini, Anthropic).
- 🎲 **Temperature:** Adjust the creativity and randomness of model responses.

## 📓 Explore Interactive Notebooks

Visit [http://localhost:8888](http://localhost:8888) to dive deeper into:

- 💬 Chat Models
- 🧑‍💻 Prompt Engineering
- 🔎 Retrieval and RAG
- 🗃️ Embedding Models & Vector Stores
- …and much more!

## 🌐 Advanced Usage: Containerized LangGraph Server

Explore powerful orchestration examples under the `langgraph/` directory. The LangGraph server is fully containerized for your convenience:

- **Access the LangGraph Studio UI:**

  [LangGraph Studio](https://smith.langchain.com/studio/?baseUrl=http://localhost:2024)

Ensure you use `localhost` (or your host IP) in the browser URL above to properly connect.

🧑‍🚀 **Graph Details:**

- 🛠️ **CodeAct Agent:** Dynamically execute Python code via LLM-driven instructions—ideal for automating tasks and integrating Python logic.
- 🌱 **Data Enrichment Agent:** Automatically enrich and categorize data, extracting insights and structuring information for intelligent workflows.

## 🤝 Contribute and Grow With Us!

We warmly welcome your contributions! Join us by:

- 📖 Adding new notebooks or examples.
- 🛠️ Improving current implementations.
- 🐞 Reporting bugs or proposing enhancements.

🎉 Happy exploring and experimenting with the limitless possibilities of LLM orchestration!