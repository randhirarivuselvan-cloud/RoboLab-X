# RoboLab X

RoboLab X is an Android-first robotics engineering workspace: describe a project in natural language, then route the request through a structured engineering pipeline for requirements, electronics, firmware, software, CAD planning, simulation, and verification.

## Current foundation

- 48 explicitly registered specialist engineering roles.
- FastAPI backend with `/healthz`, `/readyz`, `/api/status`, `/api/specialists`, `/api/generate`, and `/api/plans`.
- Provider adapter with a deterministic offline fallback.
- CORS and API rate limiting.
- Render Blueprint and production Dockerfile.
- Flutter Android client with remote API configuration through `ROBOLAB_API_URL`.
- GitHub Actions validation plus release APK/AAB build pipeline.
- Free and Pro product tiers (₹99/month, ₹799/year) represented at the API level.

## Architecture

```text
Flutter Android Client
        |
        v
RoboLab Core API
        |
        +--> Requirements / NLP
        +--> 48 specialist roles
        +--> Engineering generation
        +--> Verification / consensus (next hardening layer)
        +--> Project artifacts
        |
        v
Offline fallback OR configured AI provider
```

The specialist registry is an application architecture; it does not claim that RoboLab has trained 48 independent foundation models. A provider key is only required when cloud inference is enabled.

## Local backend

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `/docs` to inspect the API.

## Android

The Flutter client lives in `flutter_app/`. CI generates the Android platform files and builds release artifacts. For local Android development, run `flutter create --platforms=android .` inside `flutter_app`, then:

```bash
flutter pub get
flutter run --dart-define=ROBOLAB_API_URL=https://YOUR-BACKEND.onrender.com
```

For Play Store distribution, the AAB is the preferred release artifact; signing must be configured with a proper Android/Google Play signing setup. See the official Flutter release guidance: https://docs.flutter.dev/deployment/android

## Render

Connect this repository to a Render Web Service or deploy from `render.yaml`. Set `AI_API_KEY`, `AI_BASE_URL`, and `AI_MODEL` as encrypted environment variables when cloud inference is enabled. Do not commit secrets to Git.

Render uses the `/healthz` endpoint as the service health check.

## Product direction

The Pro pipeline is designed to evolve toward real cross-domain engineering verification rather than a cosmetic collection of AI labels. Future hardening should add persistent projects, authenticated users, job queues for long-running generation, compiler/test workers, circuit-rule validation, BOM/component data, simulation adapters, audit trails, and real subscription entitlement enforcement.
