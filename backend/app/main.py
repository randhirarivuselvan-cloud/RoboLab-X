import time
from collections import defaultdict, deque
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .config import get_settings
from .agents import specialist_directory, SPECIALISTS
from .agent_intelligence import enhanced_prompt
from .engineering import build_project, validate_project, synthesize_consensus
from .evaluation import evaluate_project
from .provider import generate_with_provider, ProviderError
from .premium import plan_catalog, entitlements

settings = get_settings()
app = FastAPI(title="RoboLab-X Engineering API", version="2.1.0", docs_url="/docs")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins or ["*"], allow_credentials=False, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])
_hits: dict[str, deque[float]] = defaultdict(deque)

@app.middleware("http")
async def request_context(request: Request, call_next):
    request.state.request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        key = request.client.host if request.client else "unknown"
        now = time.time(); q = _hits[key]
        while q and now - q[0] > 60: q.popleft()
        if len(q) >= settings.rate_limit_per_minute: raise HTTPException(status_code=429, detail="Rate limit exceeded")
        q.append(now)
    return await call_next(request)

class GenerateRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=12000)
    pro: bool = False
    use_ai: bool = True

@app.get("/healthz")
def healthz(): return {"status": "ok", "service": "robolab-x", "version": "2.1.0"}

@app.get("/readyz")
def readyz():
    configured = settings.ai_provider == "local" or bool(settings.ai_base_url and settings.ai_api_key and settings.ai_model)
    return {"status": "ready" if configured else "degraded", "provider_configured": configured, "provider": settings.ai_provider}

@app.get("/api/v1/info")
def info(): return {"name": "RoboLab-X", "version": "2.1.0", "specialists": 48, "pro_features": 10, "engine": "specialist-routing + verification + consensus"}

@app.get("/api/v1/agents")
def agents(): return {"count": 48, "agents": specialist_directory()}

@app.get("/api/v1/plans")
def plans(): return {"plans": plan_catalog(), "default": "free", "beta_pro_enabled": settings.pro_beta_enabled}

@app.get("/api/v1/entitlements/{plan_id}")
def get_entitlements(plan_id: str): return entitlements(plan_id)

@app.post("/api/v1/projects/generate")
async def generate(request: GenerateRequest):
    project = build_project(request.idea, request.pro)
    ai_result = None
    if request.use_ai and settings.ai_provider != "local":
        lead = next(a for a in SPECIALISTS if a.domain == "lead")
        try:
            ai_result = await generate_with_provider(
                enhanced_prompt(lead, request.idea, "Use the project plan, specialist work orders and verification results as shared context."),
                "Create a rigorous final engineering synthesis. Return JSON with decision, architecture, artifacts, risks, verification_checks, conflicts, unresolved_questions and recommended_next_steps.",
                role=lead.domain,
            )
        except ProviderError as exc:
            ai_result = {"mode": "fallback", "error": str(exc), "note": "Deterministic engineering pipeline retained."}
    findings = validate_project(project)
    quality = evaluate_project(project)
    consensus = synthesize_consensus(project, findings)
    project["ai_synthesis"] = ai_result
    project["verification"] = findings
    project["quality_evaluation"] = quality
    project["consensus"] = consensus
    return {"request_id": request.state.request_id, "project": project}

@app.get("/api/v1/pro/features")
def pro_features():
    return {"plan": "RoboLab Pro", "monthly": 99, "annual": 799, "currency": "INR", "features": plan_catalog()[1]["features"]}
