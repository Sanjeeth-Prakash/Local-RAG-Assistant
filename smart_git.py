import subprocess
import requests
import json
import sys

def get_git_diff():
    """Get the git diff of staged, unstaged, and untracked changes."""
    try:
        # Check git status first
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not status.stdout.strip():
            print("No git changes detected! Make some changes first.")
            sys.exit(0)

        diff_output = ""

        # 1. Get diff of unstaged changes
        result = subprocess.run(['git', 'diff'], capture_output=True, text=True)
        diff_output += result.stdout

        # 2. Get diff of staged changes
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
        diff_output += result.stdout

        # 3. Get content of untracked files (?? in git status)
        untracked_files = []
        for line in status.stdout.strip().split('\n'):
            if line.startswith('??'):
                filename = line[3:].strip()
                untracked_files.append(filename)

        for filename in untracked_files:
            try:
                with open(filename, 'r', errors='ignore') as f:
                    content = f.read()
                    diff_output += f"\n\n=== NEW FILE: {filename} ===\n{content}\n"
            except Exception:
                pass

        return diff_output
    except Exception as e:
        print(f"Error running git command: {e}")
        sys.exit(1)

def generate_commit_message(diff):
    """Send diff to local Ollama model to generate a commit message."""
    prompt = f"""
You are an expert software engineer. Review the following git diff and write a concise, professional git commit message following conventional commits format (e.g., feat:, fix:, refactor:).
Return ONLY the commit message, nothing else.

Git Diff:
{diff}
"""

    print("Analyzing code changes with Llama 3.1 (Local AI)...")

    response = requests.post(
        'http://127.0.0.1:11434/api/generate',
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.3
        }
    )

    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        raise Exception(f"Ollama API error: {response.text}")

if __name__ == "__main__":
    print("=== Smart Git Assistant (Day 1 Project) ===")
    diff = get_git_diff()
    commit_msg = generate_commit_message(diff)

    print("\nSuggested Commit Message:")
    print("=" * 40)
    print(commit_msg)
    print("=" * 40)
