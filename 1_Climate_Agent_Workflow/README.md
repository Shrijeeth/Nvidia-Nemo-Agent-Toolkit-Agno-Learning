# Climate Agent Workflow

Build a tool-enabled climate agent that combines an AGNO LLM with five structured tools over a bundled climate dataset. The same configuration drives the NAT CLI, FastAPI server, and integration tests.

---

## Lesson beats

1. **Create a tool-aware workflow**
   - Author `src/configs/config.yml` with `llms`, reusable tool configs, and the AGNO workflow wiring them together.
   - Implement `climate_agent_function.py` (conversation orchestration) and `climate_tool_function.py` (statistics, filtering, extremes, visualization).

2. **Ground responses in data**
   - `src/climate_agent/data/temperature_annual.csv` feeds helper utilities in `utils/climate_tools.py`.
   - Tools return JSON strings so the LLM can cite statistics, list countries, and explain trends.

3. **Run it with NAT CLI**
   - `nat run --config_file ... --input "Compare the temperature trends of Canada and Brazil..."` and other canned prompts (`make run_1_1 ... run_1_8`).

4. **Serve it as an API**
   - `nat serve --config_file ...` hosts FastAPI on `localhost:8000`.
   - Use `requests`, `curl`, or the pytest integration to call `/generate`, `/chat`, `/v1/chat/completions`.

5. **Create visualizations**
   - The `create_visualization` tool can save plots such as `climate_plot.png`, including automatic top-5 warming country charts.

6. **(optional) Connect a UI**
   - Any OpenAI-compatible chat UI can talk to `/v1/chat/completions`.
   - Try the NeMo Agent Toolkit UI manager or wire up your own frontend.

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
| `pyproject.toml` | Declares package metadata + entry-point so NAT discovers functions |
| `src/configs/config.yml` | YAML describing LLM, tool configs, and workflow wiring |
| `src/climate_agent/climate_agent_function.py` | Defines `ClimateAgentFunctionConfig` and wraps the AGNO agent |
| `src/climate_agent/climate_tool_function.py` | Registers data-grounded tools (stats, filter, extremes, list, visualization) |
| `src/climate_agent/utils/climate_tools.py` | Pandas helpers operating on `data/temperature_annual.csv` |
| `tests/integration_tests/test_api.py` | Hits REST endpoints and prints raw responses |

---

## Hands-on steps

```bash
make run_1_1  # weather vs climate
make run_1_2  # global warming delta
make run_1_3  # tougher numeric question
make run_1_4  # decade trend analysis
make run_1_5  # cross-country comparison + visualization
make run_1_6  # auto top-5 warming countries visualization
make run_1_7  # decade trend (redundant example)
make run_1_8  # per-country station + trend summary
make serve_1  # start REST API on localhost:8000
make test_api_1  # pytest integration hitting /generate, /chat, /v1/chat/completions
```

While `nat serve` is running you can also hit the endpoints manually:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What causes El Niño?"}]}'
```

---

## Next lesson teaser

- Enrich the toolset with external retrievers (NOAA, Copernicus) for fresher data.
- Introduce `nat optimize` / `nat eval` plus OpenTelemetry traces for observability.
- Hook up the official NeMo Agent Toolkit UI for a richer chat experience.
