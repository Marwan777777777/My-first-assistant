import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from memory import ResearchMemory

memory = ResearchMemory()
search_tool = DuckDuckGoSearchRun()


def build_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )


def summarize_topic(topic: str) -> tuple[str, list[dict]]:
    llm = build_llm()
    steps_log = []

    queries = [
        f"{topic} overview",
        f"{topic} how it works",
        f"{topic} latest developments 2025"
    ]

    search_results = []
    for q in queries:
        steps_log.append({"action": "🔍 Web Search", "input": q})
        try:
            result = search_tool.run(q)
            search_results.append(f"Search: {q}\nResult: {result}")
            steps_log.append({"action": "📄 Result snippet", "input": result[:300] + "..."})
        except Exception as e:
            search_results.append(f"Search: {q}\nResult: Error - {str(e)}")

    combined = "\n\n".join(search_results)
    response = llm.invoke([
        HumanMessage(content=f"""You are a Reseach Assistant. Based on these web search results, write a detailed, well-structured summary about: {topic}

Search Results:
{combined}

Write a comprehensive summary with:
- Overview
- Key concepts
- How it works
- Recent developments
- Why it matters

Format it clearly with sections.""")
    ])

    summary = response.content
    memory.save(topic, summary)
    steps_log.append({"action": "💾 Saved to memory", "input": f"Topic '{topic}' stored in ChromaDB"})

    return summary, steps_log


def ask_memory(question: str) -> str:
    llm = build_llm()
    results = memory.search(question)

    if not results:
        return "No relevant research found in memory. Try researching a topic first."

    context = "\n\n---\n\n".join([
        f"Topic: {r['topic']}\n{r['text']}" for r in results
    ])

    response = llm.invoke([
        HumanMessage(content=f"""Based on this research context, answer the question.

Context:
{context}

Question: {question}

Give a clear, helpful answer based only on the context above.""")
    ])

    return response.content