from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from Backend.app.api import auth
from Backend.app.api.interview import router as interview_router
from Backend.app.api.interview_routes import router as results_router


app = FastAPI(
    title="AI Interview Simulator",
    version="1.0.0"
)

# -------------------------------------------------
# CORS (DEV SAFE)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# ROUTERS
# -------------------------------------------------

# Auth APIs
app.include_router(auth.router)

# Interview Engine APIs
app.include_router(interview_router)

# Interview Results APIs
app.include_router(results_router)


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "AI Interview Simulator backend running",
        "docs": "/docs"
    }
