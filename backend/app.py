from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gateway import ai_gateway
from feedback_agent import log_feedback

# Initialize FastAPI
app = FastAPI(title="Math Routing Agent", version="0.1.0")

# ✅ CORS setup so React frontend (localhost:3000) can call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class QueryRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    solution: str
    feedback: str  # "good" or "bad"
    correction: str | None = None

# ✅ Health check endpoint
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Math Agent API is alive"}

# ✅ Solve math query
@app.post("/solve")
def solve_math(req: QueryRequest):
    result = ai_gateway(req.question)
    return {
        "question": req.question,
        "source": result["source"],
        "solution": result["solution"]
    }

# ✅ Feedback endpoint
@app.post("/feedback")
def give_feedback(req: FeedbackRequest):
    log_feedback(req.question, req.solution, req.feedback, req.correction)
    return {"status": "success", "message": "Feedback recorded"}
