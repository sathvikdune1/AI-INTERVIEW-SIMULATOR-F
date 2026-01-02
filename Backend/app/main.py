from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.app.api.interview import router as interview_router

app = FastAPI(
    title="AI Interview Simulator",
    version="1.0.0"
)

# -------------------------------------------------
# CORS (DEV SAFE)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# ROUTERS
# -------------------------------------------------
# IMPORTANT: interview router already has /api/interview
app.include_router(interview_router)

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "AI Interview Simulator backend running",
        "docs": "/docs"
    }
