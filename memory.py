# Simple in-memory store (no ChromaDB needed)
import json

class ResearchMemory:
    def __init__(self):
        self.entries = []

    def save(self, topic: str, summary: str):
        self.entries.append({"topic": topic, "text": summary})

    def search(self, query: str, n=3):
        if not self.entries:
            return []
        # Simple keyword match
        query_lower = query.lower()
        scored = []
        for entry in self.entries:
            score = sum(1 for word in query_lower.split() if word in entry["text"].lower() or word in entry["topic"].lower())
            scored.append((score, entry))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [e for _, e in scored[:n]]

    def count(self):
        return len(self.entries)
