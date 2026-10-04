# Self-Correcting RAG System

Level: 7 — Intermediate & Advanced RAG

Skills: Python, faithfulness check after retrieve

Score an answer against gold and context. Fail if the answer drifts.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.
