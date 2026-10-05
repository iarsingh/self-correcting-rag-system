# Self-Correcting RAG System

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/selfrag/main.py`](src/selfrag/main.py) | HTTP handlers: `GET /healthz`, `POST /evaluate` |
| [`src/selfrag/score.py`](src/selfrag/score.py) | Functions: `words`, `evaluate` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/selfrag/__init__.py`](src/selfrag/__init__.py) | Implementation or supporting configuration |
| [`tests/test_eval.py`](tests/test_eval.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn selfrag.main:app --reload
```

<!-- project-guide:end -->

Level: 7 — Intermediate & Advanced RAG

Skills: Python, faithfulness check after retrieve

Score an answer against gold and context. Fail if the answer drifts.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.
