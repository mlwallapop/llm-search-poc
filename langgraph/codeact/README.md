# Langgraph Codeact

This library implements the [CodeAct architecture](https://arxiv.org/abs/2402.01030) in LangGraph. CodeAct offers an alternative to JSON function-calling by leveraging a Turing complete language (Python in this case) to combine and transform the outputs of multiple tools. This approach is used by [Manus.im](https://manus.im/) and enables solving complex tasks in fewer steps.

## Features

- **Message History Preservation:** Message history is saved between turns to support follow-up questions.
- **Variable Persistence:** Python variables are preserved between turns, enabling more advanced follow-up queries.
- **Flexible Output:** Use `.invoke()` to get just the final result or `.stream()` to receive token-by-token output.
- **Tool Integration:** You can use any custom tools, LangChain tools, or MCP tools.
- **Model Agnostic:** Works with any model supported by LangChain (tested with Claude 3.7 so far).
- **Custom Code Sandbox:** Bring your own code sandbox via a simple functional API.
- **Customizable System Message:** Tailor the system prompt as needed.

## Installation

Install the package via pip:

```bash
pip install langgraph-codeact
```

To run the example, also install:

```bash
pip install langchain langchain-anthropic
```

## Example

The example below demonstrates a simple math agent built using CodeAct. It defines math tools, a custom evaluation function, compiles the CodeAct graph, and then streams a response to a user prompt.

### 1. Define Your Tools

Define a set of simple math functions to be used by the agent:

```python
import math

def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def sin(a: float) -> float:
    """Take the sine of a number."""
    return math.sin(a)

def cos(a: float) -> float:
    """Take the cosine of a number."""
    return math.cos(a)

def radians(a: float) -> float:
    """Convert degrees to radians."""
    return math.radians(a)

def exponentiation(a: float, b: float) -> float:
    """Raise one number to the power of another."""
    return a**b

def sqrt(a: float) -> float:
    """Take the square root of a number."""
    return math.sqrt(a)

def ceil(a: float) -> float:
    """Round a number up to the nearest integer."""
    return math.ceil(a)

tools = [
    add,
    multiply,
    divide,
    subtract,
    sin,
    cos,
    radians,
    exponentiation,
    sqrt,
    ceil,
]
```

### 2. Bring-Your-Own Code Sandbox

Supply your own code sandbox by providing a function that accepts a code string and a dictionary of local variables. **Note:** Use a secure, sandboxed environment in production. The following `eval` function is for demonstration purposes only.

```python
import builtins
import contextlib
import io
from typing import Any

def eval(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    # Store original keys before execution
    original_keys = set(_locals.keys())

    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        result = f.getvalue()
        if not result:
            result = "<code ran, no output printed to stdout>"
    except Exception as e:
        result = f"Error during execution: {repr(e)}"

    # Determine new variables created during execution
    new_keys = set(_locals.keys()) - original_keys
    new_vars = {key: _locals[key] for key in new_keys}
    return result, new_vars
```

### 3. Create the CodeAct Graph

Initialize your chat model and compile the CodeAct graph using the tools and evaluation function defined above:

```python
from langchain.chat_models import init_chat_model
from langgraph_codeact import create_codeact
from langgraph.checkpoint.memory import MemorySaver

model = init_chat_model("claude-3-7-sonnet-latest", model_provider="anthropic")

code_act = create_codeact(model, tools, eval)
agent = code_act.compile(checkpointer=MemorySaver())
```

### 4. Run It!

You can either invoke the agent to get the final result or stream the output token-by-token. The example below sends a query about a baseball scenario:

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

## Running in Development Mode

You can run the agent in development mode to test and interact with it. From the subproject's root directory, execute:

```bash
langgraph dev
```

This command launches the agent in a development environment.

## Contributing and Support

This subproject is a demonstration of the CodeAct approach in LangGraph. Feel free to adapt or extend it to suit your needs. For any issues, improvements, or suggestions, please use the appropriate channels within your organization or project management system.