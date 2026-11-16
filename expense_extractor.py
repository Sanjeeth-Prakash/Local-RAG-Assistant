"""
Automated Expense Extractor (Day 2 Project)
==========================================

What this does:
- Takes messy text (receipts, emails, Slack messages)
- Extracts expense items using local Llama 3.1
- Returns PERFECT JSON with validation

Why this matters:
- LLMs output free text (bad for production)
- Pydantic ensures data is STRUCTURED, VALID, and SAFE for databases
- This is the #1 skill in AI Engineering jobs

How it works:
1. You give messy text (e.g., receipt text)
2. Llama 3.1 extracts structured data
3. Pydantic validates it's correct JSON
4. You get clean, reliable data for your database
"""

import requests
import json
from pydantic import BaseModel, ValidationError
from typing import Optional

# ==========================================
# 1. DATA MODEL: Define EXACTLY what we want
# ==========================================
class Expense(BaseModel):
    """
    Represents ONE expense item with strict type validation.
    """
    item: str  # Name of the item (e.g., "Coffee")
    amount: float  # Amount in dollars (must be a number)
    category: Optional[str] = None  # Optional category like "food", "transport"
    date: Optional[str] = None  # Optional date (e.g., "2024-01-15")

class ExpenseList(BaseModel):
    """
    Container for a list of expenses.
    This is the exact JSON structure we want to return.
    """
    expenses: list[Expense]  # List of Expense objects

def extract_expenses(text: str) -> ExpenseList:
    """
    Extract expense items from messy text using local Llama 3.1.
    """
    print("Sending prompt to local Llama 3.1...")

    # ==============================
    # 1. Create the prompt (using double curly braces {{ }} for f-string JSON)
    # ==============================
    prompt = f"""
Extract expense information from the following text.
Return ONLY valid JSON in this exact format, no other text:

{{
  "expenses": [
    {{"item": "name of item", "amount": 0.0, "category": "category", "date": "date"}}
  ]
}}

Text to analyze:
{text}
"""

    # ==============================
    # 2. Send request to local Ollama
    # ==============================
    response = requests.post(
        'http://127.0.0.1:11434/api/generate',
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1,  # Low temperature = more deterministic/structured
        }
    )

    print("Getting raw response from Llama...")
    raw_text = response.json()['response'].strip()
    print(f"Raw response length: {len(raw_text)} characters")

    # Clean up markdown code blocks if present
    if raw_text.startswith('```'):
        raw_text = raw_text.split('\n', 1)[1]  # Remove first line
        if raw_text.endswith('```'):
            raw_text = raw_text[:-3]  # Remove closing backticks
        raw_text = raw_text.strip()

    # ==============================
    # 3. Parse and validate JSON
    # ==============================
    print("Parsing and validating JSON with Pydantic...")
    try:
        data = json.loads(raw_text)
        print("✅ Successfully parsed JSON")
        return ExpenseList(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"❌ Failed to parse: {e}")
        print(f"Raw text received was:\n{raw_text}")
        raise

if __name__ == "__main__":
    print("=== Automated Expense Extractor ===")

    # Test with messy text (like a receipt)
    messy_text = """
    I went to the store and bought coffee for $4.50 and a sandwich for $8.99.
    Also paid $12.00 for Uber on 2024-01-15.
    """

    try:
        result = extract_expenses(messy_text)
        print("\n✅ SUCCESS! Structured Data:")
        print("=" * 40)
        print(json.dumps(result.model_dump(), indent=2))
        print("=" * 40)
    except Exception as e:
        print(f"❌ Failed to extract expenses: {e}")
