#  Math Routing Agent – AI Planet Assignment

This project implements a **Math Routing Agent** using an Agentic-RAG architecture.  
It answers math questions with step-by-step solutions by combining:

- **Knowledge Base (Qdrant)** for stored problems  
- **MCP Web Search (Tavily API + SymPy validation)** as fallback  
- **AI Gateway with Guardrails** (input/output filters for math-only queries)  
- **Human-in-the-loop Feedback** (users can correct answers, corrections are stored in KB)  
- **FastAPI backend** + **React frontend** for deployment  

---

##  Features

- ✅ Knowledge Base retrieval (Qdrant)  
- ✅ Web Search fallback (MCP + Tavily API + SymPy)  
- ✅ Guardrails: block non-math queries, enforce safe answers  
- ✅ Human feedback loop with corrections added to KB  
- ✅ FastAPI backend with REST endpoints (`/solve`, `/feedback`, `/ping`)  
- ✅ React frontend with interactive UI  

---

##  Architecture

```text
User → React Frontend → FastAPI Backend → AI Gateway
     → Knowledge Base (Qdrant) OR MCP Web Search
     → Output Guardrails → User
     → Feedback → Correction stored in KB


#Project Structure
bash
Copy code
math-agent/
│── backend/            # FastAPI backend
│   └── app.py          # API endpoints
│── frontend/           # React frontend
│   └── src/App.js      # Main UI logic
│── kb/                 # Knowledge Base utilities
│   ├── prepare_kb.py   # Create KB embeddings in Qdrant
│   ├── kb_retriever.py # Retrieve answers from KB
│   └── fallback_mcp.py # Web search fallback (Tavily)
│── gateway.py          # AI Gateway with guardrails
│── feedback_agent.py   # Human feedback logging & KB update
│── math_agent.py       # Main agent logic
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation


#Setup Instructions
1. Clone Repo
bash
Copy code
git clone https://github.com/chetan10510/math-agent.git
cd math-agent
2. Backend Setup (Python 3.10+)
bash
Copy code
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
Start Qdrant (Vector DB):

bash
Copy code
docker run -p 6333:6333 -p 6334:6334 -d qdrant/qdrant
Create KB:

bash
Copy code
python kb/prepare_kb.py
Run backend:

bash
Copy code
uvicorn backend.app:app --reload --port 8000
Check API at: http://127.0.0.1:8000/docs

3. Frontend Setup (React)
bash
Copy code
cd frontend
npm install
npm start
Open: http://localhost:3000

Environment Variables
Create a .env file in project root:

ini
Copy code
TAVILY_API_KEY=your_tavily_api_key_here
Or set in PowerShell:

powershell
Copy code
setx TAVILY_API_KEY "your_tavily_api_key_here"
Demo Queries
KB Hit
mathematica
Copy code
Solve x^2 - 5x + 6 = 0
Web Fallback
pgsql
Copy code
Integrate sin(x) from 0 to pi/2
Guardrail Block
csharp
Copy code
Who is the president of USA?
Human-in-loop Feedback
vbnet
Copy code
What is the integral of x^2 from 0 to 1?
Mark answer as ❌ Bad

Enter correction → "Answer = 1/3"

Ask again → Corrected KB solution returned

#Demo Video
Demo Video Link

#Documentation
High-Level / Low-Level Design (Google Doc)

Source Code Documentation (Google Doc)

Final Proposal (Overleaf PDF)

#Author
Korivi Chetan Kumar
AI Engineer – Assignment Submission for AI Planet