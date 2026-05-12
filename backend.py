import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agent import summarize_topic, ask_memory, memory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/research")
def research(req: TopicRequest):
    try:
        summary, steps = summarize_topic(req.topic)
        return {"summary": summary, "steps": steps, "memory_count": memory.count()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
def ask(req: QuestionRequest):
    try:
        answer = ask_memory(req.question)
        return {"answer": answer, "memory_count": memory.count()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/status")
def status():
    return {"memory_count": memory.count()}
