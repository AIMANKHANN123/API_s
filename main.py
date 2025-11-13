import random
import re

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI(title="Pulse AI Question Generator")

class QuestionRequest(BaseModel):
    prompt: str
    count: int | None = None

def create_unique_questions(topic: str, n: int):
    templates = [
        f"How satisfied are you with {topic}?",
        f"What motivates you most about {topic}?",
        f"Do you feel {topic} helps improve your team's performance?",
        f"What challenges do you face in maintaining {topic}?",
        f"How can leadership enhance {topic} across teams?",
        f"On a scale of 1–10, how confident are you about {topic} results?",
        f"Do you think {topic} impacts your productivity positively?",
        f"How would you rate communication around {topic}?",
        f"Would you recommend our approach to {topic} to others?",
        f"How often do you engage in activities related to {topic}?",
        f"What suggestions do you have to strengthen {topic}?",
        f"Do you feel supported by management regarding {topic}?",
        f"How can your team better handle {topic} issues?",
        f"What best practices could improve {topic}?",
        f"How important is {topic} for achieving company goals?",
        f"Do you think your peers understand the value of {topic}?",
        f"What’s one change you’d like to see in how we approach {topic}?",
        f"Have you received feedback or recognition related to {topic}?",
        f"How would you describe your experience with {topic}?",
        f"What steps can improve awareness around {topic}?",
        f"How well does {topic} align with your personal growth?",
        f"Do you believe {topic} contributes to job satisfaction?",
        f"What are the barriers preventing better {topic}?",
        f"How can {topic} be measured effectively?",
        f"Do you think our company culture supports {topic}?",
    ]
    random.shuffle(templates)
    selected = (templates * ((n // len(templates)) + 1))[:n]

    question_types = ["binary", "scale", "open-ended", "nps-style"]
    return [{"question": q, "type": random.choice(question_types)} for q in selected]

@app.get("/")
def read_root():
    return {"message": "Pulse AI Question Generator is running. Use /generate endpoint to POST."}

@app.post("/generate")
def generate_questions(req: QuestionRequest = Body(...)):
    prompt = req.prompt.lower()
    topics_data = []

    # Improved regex to detect multiple "X questions about Y" patterns
    matches = re.findall(r"(\d+)\s*(?:questions\s*)?about\s*([a-zA-Z\s]+?)(?=\s+and\s+\d+\s*questions\s*about|$)", prompt)
    
    if matches:
        for count, topic in matches:
            count = min(int(count), 100)
            topic = topic.strip()
            questions = create_unique_questions(topic, count)
            topics_data.append({
                "topic": topic,
                "count": len(questions),
                "questions": questions
            })
    else:
        topic_match = re.search(r"about\s+([\w\s]+)", prompt)
        topic = topic_match.group(1).strip() if topic_match else "workplace"
        count = min(req.count if req.count else 10, 100)
        questions = create_unique_questions(topic, count)
        topics_data.append({
            "topic": topic,
            "count": len(questions),
            "questions": questions
        })
    
    total = sum([t["count"] for t in topics_data])
    return {"prompt": req.prompt, "total_generated": total, "results": topics_data}
