# MW.AI — Research Assistant

> Research a topic. Ask questions. It remembers everything.

A personal AI research assistant that combines RAG, live web search, and persistent memory into one interface. Feed it a topic, let it research, then ask it anything about what it learned.

## What It Does

Two modes in one interface:

**Research Mode** — Enter any topic and the assistant searches the web via DuckDuckGo, retrieves relevant information, and stores it in memory for querying.

**Memory Mode** — Ask natural language questions about anything the assistant has already researched. Answers are grounded in retrieved sources, not hallucinated.

## Stack

| Layer | Technology |
|---|---|
| LLM | Gemini |
| Framework | LangChain |
| Web Search | DuckDuckGo |
| API | FastAPI |
| Frontend | HTML/CSS/JS |

## Features

- Live web research on any topic
- Persistent memory across queries
- Source-grounded answers
- Clean split interface — research left, ask right
- Memory counter showing stored items

## Run It

```bash
git clone https://github.com/Marwan7777777/My-first-assistant
cd My-first-assistant
pip install -r requirements.txt
python main.py
```

Open `index.html` in your browser or visit `http://localhost:8000`

## How It Works

1. Enter a topic in Research mode → hits DuckDuckGo → chunks and embeds results
2. Results stored in memory
3. Ask questions in Memory mode → RAG retrieves relevant chunks → Gemini answers from sources

---

*Built by [Marwan Mahmoud](https://www.linkedin.com/in/marwan-mahmoud-78a2aa371) — Cairo, Egypt*
