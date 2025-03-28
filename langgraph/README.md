# 🌐 LangGraph: Advanced LLM Orchestration and Agent Frameworks

Welcome to the LangGraph section! Here you'll find advanced demonstrations and frameworks designed to orchestrate and manage powerful Large Language Model (LLM)-driven agents and workflows.

## 🚀 What's Inside?

### 🛠️ CodeAct Agent

- **Dynamic Code Execution:** Enables LLMs to dynamically generate and execute Python code, facilitating powerful automation and complex task handling.
- **Interactive Exploration:** Ideal for tasks requiring custom logic and Python-based integrations within conversational interfaces.

**Example Invocation:**

You can interact with the CodeAct agent by providing a query, such as:

```python
messages = [{
    "role": "user",
    "content": "A batter hits a baseball at 45.847 m/s at an angle of 23.474° above the horizontal. The outfielder, who starts facing the batter, picks up the baseball as it lands, then throws it back towards the batter at 24.12 m/s at an angle of 39.12 degrees. How far is the baseball from where the batter originally hit it? Assume zero air resistance."
}]

for typ, chunk in agent.stream(
    {"messages": messages},
    stream_mode=["values", "messages"],
    config={"configurable": {"thread_id": 1}},
):
    if typ == "messages":
        print(chunk[0].content, end="")
    elif typ == "values":
        print("\n\n---answer---\n\n", chunk)
```

### 🌱 Data Enrichment Agent

- **Automated Data Processing:** Automatically enrich, classify, and structure your data using intelligent LLM-driven workflows.
- **Contextual Understanding:** Extract meaningful insights from data, categorize information, and enhance content through context-aware processing.

**Example Invocation:**

You can invoke the Data Enrichment agent by providing structured input, such as:

```python
input_data = {
    "text": "Apple releases the new iPhone 15 with advanced camera features and improved battery life."
}

enriched_output = enrichment_agent.invoke(input_data)
print(enriched_output)
```

This example demonstrates how the agent can automatically classify and enrich the provided text data.

## 🛠️ Getting Started

1. **Install Dependencies:** Ensure your environment has all required packages installed:

```bash
pip install -r requirements.txt
```

2. **Run LangGraph:** Start experimenting from the project's root:

```bash
langgraph dev
```

## 📁 Directory Structure

- **`codeact/`:** Contains implementations and examples demonstrating dynamic code execution.
- **`data-enrichment-agent-python/`:** Contains scripts and configurations for intelligent data enrichment workflows.

## 🤝 Contributing

We're excited to have your contributions!

- 📖 Add new use-case examples or agents
- 🚀 Improve existing workflows
- 🐛 Report issues and propose solutions

Dive in and push the boundaries of LLM orchestration! 🌟

