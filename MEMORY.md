# AI/ML Engineering Bootcamp - Job Ready Documentation
# Session: 2026-11-16 | Location: D:\OmniRoute

## ✅ DAY 1 COMPLETED — Smart Git Assistant

### What You Built
- Local Ollama AI server running on RTX 3070 GPU
- Symbolic link redirecting model storage from C: drive to G: drive
- Python scripts that talk to local Llama 3.1 model
- Smart Git Assistant that reads git diffs and writes AI commit messages

### Files Created
| File | Purpose | Run Command |
|------|---------|-------------|
| `test_ai.py` | Tests Ollama connection & model response | `python test_ai.py` |
| `smart_git.py` | Reads git changes, AI generates commit message | `python smart_git.py` |
| `requirements.txt` | Python dependencies | `pip install -r requirements.txt` |

### Concepts Learned (Day 1)
**Ollama**: Local AI server that runs LLMs on your machine. No API keys needed. Models run locally on your GPU.

**LLM (Large Language Model)**: A massive AI trained on internet text. Llama 3.1 8B = 8 billion parameters (about 16GB file size).

**GPU Acceleration**: Your RTX 3070 GPU processes the model much faster than CPU alone. Models load into VRAM (video memory).

**Symbolic Link (Junction)**: A Windows shortcut that tricks programs into writing to C: but actually saves to G:. Prevents C: drive from filling up.

**Git Diff**: Shows what code changed in your repo. We feed this to AI to auto-write commit messages.

---

## 🚀 DAY 2 — Structured Data & Function Calling (In Progress)

### What We're Building
**Automated Expense Extractor**: Takes messy text (receipts, emails), returns perfect JSON for databases.

### Files Created
| File | Purpose | Run Command |
|------|---------|-------------|
| `expense_extractor.py` | Extracts expenses from text → validated JSON | `python expense_extractor.py` |

### Concepts Learned (Day 2)

**JSON (JavaScript Object Notation)**: Lightweight data format used everywhere in web development and AI. Example:
```json
{"expenses": [{"item": "coffee", "amount": 4.50}]}
```

**Pydantic**: Python library that validates data. Acts like a "security guard" for your data:
- Ensures numbers are numbers, strings are strings
- Throws errors if AI returns wrong format
- Converts types automatically

**Why Structured Data Matters**: Companies can't use free-form AI text in databases. They need JSON with exact fields. Pydantic guarantees this.

**Temperature Setting**: Controls AI randomness.
- `0.1` = deterministic, structured output (good for JSON)
- `0.7` = creative, conversational output (good for chat)

---

## 📁 File Structure (D:\OmniRoute)
```
D:\OmniRoute\
├── hello-world.html
├── index.html
├── src/
├── style.css
├── requirements.txt
├── test_ai.py
├── test_ai.py
├── smart_git.py
├── expense_extractor.py
└── test.txt
```

---

## 🔧 Run Commands Cheat Sheet

| Task | Command |
|------|---------|
| Install Python deps | `pip install -r requirements.txt` |
| Test Ollama connection | `python test_ai.py` |
| Smart Git Assistant | `python smart_git.py` |
| Expense Extractor | `python expense_extractor.py` |
| Check git status | `git status` |
| Install Ollama package | `pip install ollama` |

---

## 🐛 Debug Guide

### "Connection failed: Read timed out"
**Cause**: Model loading into GPU VRAM takes time on first run.
**Fix**: Increase `timeout` parameter in `requests.post()` to 120 seconds.

### "Not a git repository"
**Cause**: No `.git` folder in directory.
**Fix**: Run `git init` once, then commit your files.

### "SyntaxError: f-string single '}' is not allowed"
**Cause**: JSON inside Python f-string needs double curly braces `{{` and `}}`.
**Fix**: Use `{{` for `{` and `}}` for `}` inside f-strings.

### "Ollama not responding"
**Cause**: Ollama app not running in taskbar.
**Fix**: Open Ollama from Windows Start menu, wait for llama icon in taskbar.

---

## 🎯 Job-Ready Skills Tracked

| Skill | Status |
|-------|--------|
| Local LLM deployment (Ollama) | ✅ Day 1 |
| GPU-accelerated AI inference | ✅ Day 1 |
| API integration with Python | ✅ Day 1 |
| Git + AI automation | ✅ Day 1 |
| Structured data extraction (JSON) | 🔄 Day 2 |
| Pydantic data validation | 🔄 Day 2 |
| Function calling / Tool use | ⏳ Day 2 |
| RAG (Retrieval Augmented Generation) | ⏳ Day 3 |
| Vector databases | ⏳ Day 3-4 |
| AI Agents | ⏳ Day 5 |
| Observability & Testing | ⏳ Day 6 |
| Full-stack AI Portfolio Project | ⏳ Day 7 |

---

## 📝 Instructions for Claude (Working Protocol)

### Every time we create files:
1. I write the complete file to `D:\OmniRoute\`
2. I explain every line of code and concept
3. You run the file in your VS Code terminal
4. You report the output
5. If errors occur, I debug and fix

### Code explanation format:
- **What it does**: One sentence summary
- **How it works**: Step-by-step breakdown
- **Why it matters**: Job-ready context
- **Key terms**: Bolded with definitions

### Terminal usage:
- Use VS Code terminal only (no PowerShell unless needed)
- Run commands from `D:\OmniRoute\` directory
- Python commands: `python filename.py`
- Install packages: `pip install package-name`

---

## 🏁 Next Steps
After Day 2 completes:
1. Day 3: RAG Part 1 (Embeddings & Vector Databases)
2. Day 4: RAG Part 2 (Advanced Retrieval + Caching)
3. Day 5: AI Agents (Tool use, loops, ReAct pattern)
4. Day 6: Testing & Observability (LLM-as-judge, metrics)
5. Day 7: Portfolio Project (Full-stack AI Support Engineer)

**Goal**: By end of Week 1, you'll have 5+ production-ready AI projects in your portfolio.
