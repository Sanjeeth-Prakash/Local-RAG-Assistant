import requests

def test_ollama():
    print("Testing connection to local Ollama (Llama 3.1 8B)...")
    print("(Note: First run might take 30-60 seconds as the model loads into your RTX 3070 VRAM)")
    try:
        response = requests.post(
            'http://127.0.0.1:11434/api/generate',
            json={
                "model": "llama3.1",
                "prompt": "Say 'Ollama is ready!' and explain what a token is in one sentence.",
                "stream": False,
                "temperature": 0.7
            },
            timeout=120  # Increased timeout for first model load
        )

        if response.status_code == 200:
            result = response.json()
            print("\nSUCCESS! AI Response:")
            print("-" * 40)
            print(result['response'])
            print("-" * 40)
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure Ollama is running in your taskbar!")

if __name__ == "__main__":
    test_ollama()