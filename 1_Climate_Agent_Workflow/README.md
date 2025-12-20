# Climate Agent Workflow

Build a minimal climate-focused agent, run it via the NAT CLI, and serve the exact same configuration as a REST API so external clients (or the NeMo UI) can call it.

---

## Lesson beats

1. **Create a minimal workflow**
   - Author `src/configs/config.yml` with two sections: `llms` (our `climate_llm` NIM endpoint) and `workflow` (the AGNO function we register).
   - Implement `climate_agent_function.py` to fetch the LLM, apply a climate-specific system prompt, and expose `_arun` so NAT can execute it.

2. **Run it with NAT CLI**
   - `nat run --config_file ... --input "What is the difference between weather and climate?"`
   - Repeat with additional prompts to see deterministic vs knowledge-limited responses.

3. **Serve it as an API**
   - `nat serve --config_file ...` hosts FastAPI on `localhost:8000`.
   - Use `requests` or the provided pytest to call `/generate`, `/chat`, `/v1/chat/completions`.

4. **(optional) Connect a UI**
   - Any OpenAI-compatible chat UI can talk to `/v1/chat/completions`.
   - Try the NeMo Agent Toolkit UI manager or wire up your own frontend.

5. **Inspect limitations**
   - Because this workflow is “LLM-only”, answers rely solely on model training data.
   - Follow-up lessons should add tools/retrievers to ground outputs with real climate data.

---

## Prerequisites

From the repo root:

```bash
make install_dependencies   # installs uv
make install_1              # editable install of this workflow
make validate_1             # optional: nat validate --config_file ...
```

Ensure `.env` is populated + exported (see root README).

---

## Workflow anatomy

| Component | Purpose |
|-----------|---------|
| `pyproject.toml` | Declares package metadata + entry-point so NAT discovers the function |
| `src/climate_agent/climate_agent_function.py` | Defines `ClimateAgentFunctionConfig` + AGNO agent |
| `src/configs/config.yml` | Minimal YAML describing LLM and workflow wiring |
| `tests/integration_tests/test_api.py` | Hits REST endpoints and prints raw responses |

---

## Hands-on steps

```bash
make run_1_1  # Ask: “What is the difference between weather and climate?”
make run_1_2  # Ask: “How much has global average temperature increased…?”
make run_1_3  # Ask a harder data-heavy question
make serve_1  # Start REST API on localhost:8000
make test_api_1  # GET printed JSON from /generate, /chat, /v1/chat/completions
```

While `nat serve` is running you can also hit the endpoints manually:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What causes El Niño?"}]}'
```

---

## Next lesson teaser

- Add tools / retrieval (e.g., NOAA datasets) so the agent stops hallucinating numbers.
- Introduce `nat optimize` / `nat eval` to tighten prompts and monitor quality.
- Hook up the official NeMo Agent Toolkit UI for a richer chat experience.
