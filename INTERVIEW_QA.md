# self-correcting-rag-system — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does self-correcting-rag-system address, and what can you demonstrate?

Score an answer against gold and context. Fail if the answer drifts.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/selfrag/main.py`](src/selfrag/main.py): Implementation or supporting configuration.
- [`src/selfrag/score.py`](src/selfrag/score.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/selfrag/__init__.py`](src/selfrag/__init__.py): Implementation or supporting configuration.
- [`tests/test_eval.py`](tests/test_eval.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `evaluate` and explain the decision it makes?

The main walkthrough here is `evaluate(answer, gold, context)` in [`src/selfrag/score.py`](src/selfrag/score.py#L10).

```python
def evaluate(answer, gold, context):
    aw, gw, cw = words(answer or ""), words(gold or ""), words(context or "")
    faithfulness = len(aw & cw) / len(aw) if aw else 0
    correctness = len(aw & gw) / len(gw) if gw else 0
    return {
        "faithfulness": round(faithfulness, 4),
        "correctness": round(correctness, 4),
        "passed": faithfulness >= 0.5 and correctness >= 0.5,
    }
```

The implementation calls `len`, `round`, `words`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `words` have?

`words(text)` is defined in [`src/selfrag/score.py`](src/selfrag/score.py#L6).

Its return expressions include:

- `set(re.findall('[a-z0-9]+', text.lower())) - STOP`

It uses `re.findall`, `set`, `text.lower`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. Where would you add input-validation tests?

Start with the handlers `healthz` in [`src/selfrag/main.py`](src/selfrag/main.py#L8), `post_evaluate` in [`src/selfrag/main.py`](src/selfrag/main.py#L13). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_eval.py`](tests/test_eval.py#L7) contains `test_pass_and_fail`:

```python
def test_pass_and_fail():
    good = client.post("/evaluate", json={"answer": 'The platform refuses latest tags.', "gold": 'The platform refuses latest tags.', "context": 'The platform refuses latest tags in production.'}).json()
    assert good["passed"] is True
    bad = client.post("/evaluate", json={"answer": "The cafeteria serves soup.", "gold": 'The platform refuses latest tags.', "context": 'The platform refuses latest tags in production.'}).json()
    assert bad["passed"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/selfrag/main.py`](src/selfrag/main.py#L8).
- `POST /evaluate` → `post_evaluate` in [`src/selfrag/main.py`](src/selfrag/main.py#L13).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `STOP` in [`src/selfrag/score.py`](src/selfrag/score.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `evaluate`?

In [`src/selfrag/score.py`](src/selfrag/score.py#L10), `evaluate(answer, gold, context)` receives the inputs. The function computes these intermediate values:

- `aw, gw, cw = (words(answer or ''), words(gold or ''), words(context or ''))`
- `faithfulness = len(aw & cw) / len(aw) if aw else 0`
- `correctness = len(aw & gw) / len(gw) if gw else 0`

Its result is defined by:

- `{'faithfulness': round(faithfulness, 4), 'correctness': round(correctness, 4), 'passed': faithfulness >= 0.5 and correctness >= 0.5}`
