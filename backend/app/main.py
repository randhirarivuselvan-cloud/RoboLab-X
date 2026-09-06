import time
from collections import defaultdict, deque
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .config import get_settings
from .agents import specialist_directory
from .engineering import build_project, validate_project, synthesize_consensus

settings = get_settings()
app = FastAPI(title="RoboLab-X API", version="1.0.0", docs_url="/docs")

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

_hits: dict[str, deque[float]] = defaultdict(deque)

@app.middleware("http")
async def request_context(request: Request, call_next):
    request.state.request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        key = request.client.host if request.client else "unknown"
        now = time.time()
        q = _hits[key]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= settings.rate_limit_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        q.append(now)
    return await call_next(request)

class GenerateRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=12000)
    pro: bool = False

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "robolab-x"}

@app.get("/readyz")
def readyz():
    provider_ready = settings.ai_provider == "local" or bool(settings.ai_base_url and settings.ai_api_key)
    return {"status": "ready" if provider_ready else "degraded", "provider_configured": provider_ready}

@app.get("/api/v1/info")
def info():
    return {"name": "RoboLab-X", "version": "1.0.0", "specialists": 48, "pro_features": 8}

@app.get("/api/v1/agents")
def agents():
    return {"count": 48, "agents": specialist_directory()}

@app.post("/api/v1/projects/generate")
def generate(request: GenerateRequest):
    project = build_project(request.idea, request.pro)
    findings = validate_project(project)
    consensus = synthesize_consensus(project, findings)
    project["verification"] = findings
    project["consensus"] = consensus
    return {"project": project}

@app.get("/api/v1/pro/features")
def pro_features():
    return {
        "plan": "RoboLab Pro",
        "monthly": 99,
        "annual": 799,
        "features": [
            "advanced_generation", "consensus", "power_analysis", "firmware_review",
            "cad_spec", "simulation_plan", "project_export", "priority_generation"
        ],
    }
