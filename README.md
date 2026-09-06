# RoboLab-X

Professional AI-assisted robotics engineering workspace for Android.

## Product architecture

Flutter Android client → FastAPI backend → RoboLab Core → specialist engineering agents → verification → consensus → project artifact.

RoboLab-X deliberately separates **specialist agents** from the underlying AI provider. The 48 specialists are domain-specific orchestration roles; they are not falsely represented as 48 independently trained foundation models.

## Included in this foundation

- Production-oriented FastAPI API
- `/healthz` and `/readyz` probes
- CORS configuration
- Request correlation IDs
- Basic in-process rate limiting
- 48 registered engineering specialist roles
- Deterministic validation layer
- Consensus synthesis layer
- Free/Pro capability policy
- Project generation endpoint
- JSON project export
- Flutter Android client
- Render deployment configuration
- Docker deployment
- GitHub Actions CI
- Secure server-side AI configuration via environment variables

## Run backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Flutter client

```bash
cd app
flutter pub get
flutter run
```

Set the backend URL with:

```bash
flutter run --dart-define=ROBOLAB_API_URL=https://your-service.onrender.com
```

Never place an AI provider secret in Flutter or in the APK.

## Environment

Copy `backend/.env.example` to your deployment environment. `AI_API_KEY` is optional for the deterministic/local foundation and is only required when an external provider is configured.

## Deployment

Render can deploy the backend from `render.yaml`. GitHub Actions validates Python and Flutter code on pushes and pull requests.
