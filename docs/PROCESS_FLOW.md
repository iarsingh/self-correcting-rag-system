# Self-Correcting RAG System: process flows

## Domain request

Endpoint: `POST /evaluate`. Stages summarize [src/selfrag/score.py](../src/selfrag/score.py). This is in-process Python, not a hosted model or production apply.

```mermaid
flowchart TD
  A["POST /evaluate"] --> B{"Valid input?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes: answer/gold/context strings"| C["Domain function in score.py"]
  C --> O["faithfulness and correctness ratios; no rewrite"]
  O --> X["No production side effect"]
```

See [INTERVIEW_QA.md](../INTERVIEW_QA.md) for fixture walkthroughs and [PROJECT_ARCHITECTURE.md](../PROJECT_ARCHITECTURE.md) for the component map.
