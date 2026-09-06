from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from .app.config import settings
from .app.agents import list_specialists
from .app.ai import generate, AIError

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
app = FastAPI(title=settings.app_name, version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: __import__('fastapi').responses.JSONResponse(status_code=429, content={"detail":"Rate limit exceeded"}))
app.add_middleware(SlowAPIMiddleware)
origins = [x.strip() for x in settings.allowed_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins if origins != ["*"] else ["*"], allow_credentials=origins != ["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/healthz")
async def healthz():
    return {"status":"ok","service":"robolab-x"}

@app.get("/readyz")
async def readyz():
    return {"status":"ready","ai_mode":"provider" if settings.ai_api_key and settings.ai_base_url and settings.ai_model else "offline"}

@app.get("/api/status")
async def status():
    return {"name":settings.app_name,"version":"1.0.0","environment":settings.environment,"specialists":48,"pro":True}

@app.get("/api/specialists")
async def specialists():
    return {"count":48,"agents":list_specialists()}

@app.post("/api/generate")
@limiter.limit(settings.rate_limit)
async def generate_project(request: Request):
    body = await request.json()
    prompt = str(body.get("prompt", "")).strip()
    if not prompt:
        return __import__('fastapi').responses.JSONResponse(status_code=422, content={"detail":"prompt is required"})
    try:
        result = await generate(prompt, body.get("context"))
        return {"ok":True,"result":result,"mode":"provider" if settings.ai_api_key else "offline","agents_consulted":48}
    except AIError as exc:
        return __import__('fastapi').responses.JSONResponse(status_code=503, content={"ok":False,"detail":str(exc)})

@app.get("/api/plans")
async def plans():
    return {"plans":[
        {"id":"free","name":"RoboLab Free","price_inr":0,"features":["Core builder","Basic project analysis","Offline fallback"]},
        {"id":"pro_monthly","name":"RoboLab Pro","price_inr":99,"billing":"monthly","features":["48-specialist pipeline","Consensus review","Advanced validation","Firmware review","Power-path analysis","CAD-ready specifications","Simulation planning","Project export","Priority generation"]},
        {"id":"pro_yearly","name":"RoboLab Pro Annual","price_inr":799,"billing":"yearly","features":["Everything in Pro","Annual billing"]}
    ]}
