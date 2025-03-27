# Langgraph Codeact Math Agent Subproject

This subproject demonstrates a simple agent that leverages Langgraph's Codeact framework to execute Python code based on chat prompts. It features custom evaluation and a set of math tools to perform various computations.

## Overview

The agent is built to:

- **Execute Code Dynamically:**  
  A custom `eval` function runs provided Python code, capturing any printed output and any new variables created during execution.
  
- **Provide Math Tools:**  
  A set of math functions (such as add, multiply, divide, subtract, sin, cos, radians, exponentiation, sqrt, and ceil) is defined to support various mathematical operations.
  
- **Integrate a Chat Model:**  
  The agent initializes a chat model (using Anthropic's `claude-3-7-sonnet-latest` via Langchain) to process user prompts.
  
- **Stream Results:**  
  The agent streams its responses in real time, enabling interactive problem solving.

## How It Works

### Evaluation Function

The `eval` function:
- Executes arbitrary Python code using `exec`.
- Captures any printed output via a redirected `stdout`.
- Returns both the output and any new variables defined during execution.

### Math Tools

The following functions are available as callable tools:

- **add(a, b):** Returns the sum of `a` and `b`.
- **multiply(a, b):** Returns the product of `a` and `b`.
- **divide(a, b):** Returns the result of dividing `a` by `b`.
- **subtract(a, b):** Returns the difference between `a` and `b`.
- **sin(a):** Returns the sine of `a`.
- **cos(a):** Returns the cosine of `a`.
- **radians(a):** Converts degrees to radians.
- **exponentiation(a, b):** Returns `a` raised to the power of `b`.
- **sqrt(a):** Returns the square root of `a`.
- **ceil(a):** Rounds `a` up to the nearest integer.

### Agent Initialization and Execution

1. **Chat Model Initialization:**  
   The chat model is initialized using Langchain’s `init_chat_model`, configured to use Anthropic’s `claude-3-7-sonnet-latest`.

2. **Agent Compilation:**  
   The `create_codeact` function compiles the agent using the defined math tools and evaluation function. A memory-based checkpointer (`MemorySaver`) is used to maintain state.

3. **Execution Example:**  
   In the main block, a baseball projectile motion prompt is sent to the agent. The agent processes the prompt, streams its messages, and prints the computed answer.

## Installation and Setup

1. **Install Dependencies:**  
   Ensure you have the required packages installed. For example:
   ```bash
   pip install langchain langgraph_codeact
   ```
   *(Include any additional dependencies as needed.)*

2. **Configure API Credentials:**  
   Set up your API credentials for Anthropic and any other services according to their documentation.

## Running the Agent

To run the agent, execute the following command from the subproject's root directory:
```bash
python math_example.py
```

Alternatively, you can launch the agent in development mode by running:
```bash
langgraph dev
```
This command starts the agent in a development environment, allowing you to test and interact with it.

## Contributing and Support

This subproject is provided as a working example. Feel free to adapt or extend it to fit your needs. For any issues, improvements, or suggestions, please use the appropriate communication channels or file an issue if integrated within a larger project.