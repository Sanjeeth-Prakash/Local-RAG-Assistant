"""
AI Calculator with Function Calling (Tool Use) - Day 2.5
=========================================================

WHAT THIS TEACHES:
- "Function Calling" = giving the AI a list of TOOLS it can use
- The AI DECIDES which tool to call and what arguments to pass
- Your Python code EXECUTES the tool and returns the result
- This is the foundation of AI AGENTS (Day 5)

WHY IT MATTERS FOR JOBS:
- This is the pattern behind AI agents (Claude Code, ChatGPT tools, etc.)
- Companies hire for this EXACT skill
- It lets AI DO things, not just SAY things

HOW IT WORKS:
1. We define "tools" = Python functions the AI is allowed to call
2. We tell Ollama "here are your available tools" (the schema)
3. The AI generates a "tool call" (which tool + what arguments)
4. We execute that tool in Python and return the result
"""

import requests
import json

# ==========================================
# 1. DEFINE THE TOOLS (Python functions)
# ==========================================
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b. Raises error if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# ==========================================
# 2. TOOL SCHEMAS (Tell the AI what tools exist)
# ==========================================
# This is the "menu" we give the AI. It describes each tool's
# name, description, and parameters so the AI knows how to call it.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtract the second number from the first",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide the first number by the second",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
]

# ==========================================
# 3. TOOL EXECUTOR (Runs the actual Python function)
# ==========================================
def execute_tool(name: str, arguments: dict):
    """Given a tool name and arguments, run the actual Python function."""
    # Map tool name -> function
    tool_map = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if name not in tool_map:
        return f"Error: Unknown tool '{name}'"

    try:
        # Call the function with the arguments
        result = tool_map[name](**arguments)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# 4. AI AGENT LOOP (The core pattern)
# ==========================================
def ai_calculate(expression: str):
    """
    The "agent" that:
    1. Asks AI what to do (with tool menu)
    2. Gets back a tool call
    3. Executes the tool
    4. Returns result
    """
    prompt = f"""
You are a math calculator assistant.
Given the user's math question, decide which tool to use and what numbers to pass.

User question: {expression}

IMPORTANT: You must use one of your available tools (add, subtract, multiply, divide) to solve it.
"""

    print(f"🤖 Asking Llama 3.1 how to solve: '{expression}'")
    print(f"   Available tools: add, subtract, multiply, divide")

    # Send to Ollama with tools enabled
    response = requests.post(
        'http://127.0.0.1:11434/api/chat',
        json={
            "model": "llama3.1",
            "messages": [{"role": "user", "content": prompt}],
            "tools": TOOLS,  # <-- THE KEY: give the AI its tool menu
            "stream": False,
        }
    )

    data = response.json()
    message = data.get('message', {})

    # Check if the AI wants to call a tool
    if message.get('tool_calls'):
        tool_call = message['tool_calls'][0]  # Take first tool call
        tool_name = tool_call['function']['name']
        tool_args = tool_call['function']['arguments']

        print(f"🧠 AI decided to call: {tool_name}({json.dumps(tool_args)})")

        # Execute the tool in Python
        result = execute_tool(tool_name, tool_args)
        print(f"✅ Tool returned: {result}")

        # Give the result back to the AI so it can answer the user
        second_response = requests.post(
            'http://127.0.0.1:11434/api/chat',
            json={
                "model": "llama3.1",
                "messages": [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": "", "tool_calls": [tool_call]},
                    {"role": "tool", "content": str(result)},
                ],
                "stream": False,
            }
        )

        final = second_response.json()
        print(f"💬 AI final answer: {final['message']['content']}")
        return final['message']['content']

    else:
        print(f"💬 AI answered directly: {message.get('content', 'No response')}")
        return message.get('content', 'No response')

# ==========================================
# 5. MAIN
# ==========================================
if __name__ == "__main__":
    print("=== AI Calculator with Function Calling ===")

    # Test cases: AI has to DECIDE which tool to use
    test_questions = [
        "What is 15 plus 27?",
        "What is 100 minus 37?",
        "What is 12 times 8?",
        "What is 144 divided by 12?",
    ]

    for q in test_questions:
        print("\n" + "=" * 50)
        result = ai_calculate(q)
        print(f"Question: {q}")
        print(f"Answer: {result}")
        print("=" * 50)
