# NVIDIA NeMo Agent Toolkit – Learning Journey

Welcome! This repo tracks a hands-on course for building **enterprise-ready agents** with NVIDIA’s open-source NeMo Agent Toolkit (NAT). You’ll go from a fragile demo to production-grade workflows that are observable, deployable, and easy to iterate on.

The material is inspired by NVIDIA & DeepLearning.AI’s curriculum (taught by Brian McBrayer) and focuses on solving the classic AI Agents Production Problems:

- **Observability:** trace tool calls, model choices, and performance hotspots via OpenTelemetry.
- **Evaluation & optimization:** run disciplined evals, catch regressions, and tune agents automatically.
- **Deployment:** package agent workflows as APIs with auth, rate limits, and CI/CD-friendly configs.

Each folder in this repo represents a milestone in that journey, starting with a climate-analysis agent that grows from a single LLM call into a multi-agent, instrumented system; in this snapshot the `1_Climate_Agent_Workflow` now wires five AGNO tools atop the base LLM, ships a bundled `temperature_annual.csv` dataset with helper utilities, exposes visualization commands like `make run_1_5`/`run_1_6`, expands the canned prompts through `make run_1_1 ... run_1_8`, and keeps the familiar NAT ergonomics (`nat validate`, `nat serve`, integration tests) unchanged.

---

## Day 1 vs Day 2

| Challenge | Why it matters | NAT capability |
|-----------|----------------|----------------|
| Integration complexity | Agents mix LangChain, CrewAI, custom Python | Config-driven orchestration + reusable components |
| Repeatability | Small prompt/model tweaks can flip outcomes | Versioned configs + systematic evals |
| Observability | Need traces for “wrong tool call” bugs | OpenTelemetry → Phoenix (or any backend) |
| Deployment | APIs, auth, rate limits, monitoring | `nat serve`, YAML-first API definition |
| Performance & cost | Token hotspots hidden in nested calls | Profilers + optimizer (Optuna / genetic search) |

---

## Environment setup

1. Copy `.env.example` → `.env` and fill in secrets (`NVIDIA_BASE_URL`, `NVIDIA_API_KEY`, `PHOENIX_ENDPOINT`, `PHOENIX_PROJECT`, `PHOENIX_API_KEY`, etc.).
2. Export them using the Make helper:

| Shell | Command |
|-------|---------|
| macOS / Linux | `source <(make env)` |
| PowerShell | `make env TARGET_SHELL=env-pwsh \| Invoke-Expression` |
| cmd.exe | `for /f "delims=" %i in ('make env TARGET_SHELL=env-cmd') do %i` |

---

## Repository map

| Folder | Description |
|--------|-------------|
| `1_Climate_Agent_Workflow/` | Tool-enabled climate agent (LLM + AGNO tools, LangGraph calculator, dataset, visualizations) |
| `scripts/` | Utility helpers (env management, etc.) |
| `Makefile` | Convenience targets: install, validate, run, serve, test |

Future lessons (e.g., `2_Tools_Workflow`, `3_MultiAgent_Workflow`) will continue expanding observability plumbing, evaluation suites, optimizers, and UI integrations.

---

## Quickstart commands (from repo root)

```bash
make install_dependencies   # install uv
make install_1              # uv editable install of the first workflow
make validate_1             # nat validate --config_file ...
make run_1_1                # weather vs climate
make run_1_2                # global warming delta
make run_1_3                # tougher numeric question
make run_1_4                # decade trend analysis
make run_1_5                # cross-country comparison + visualization
make run_1_6                # auto top-5 warming countries visualization
make run_1_7                # decade trend (redundant example)
make run_1_8                # per-country station + trend summary
make run_1_9                # emissions scenario needing calculator agent
make serve_1                # expose FastAPI on localhost:8000
make test_api_1             # hit /generate, /chat, /v1/chat/completions and print responses
```

Need to see API output? Run `make serve_1` in one terminal and `make test_api_1` (or the curl examples in the workflow README) in another. Observability + eval tooling arrives in later lessons when we wire up Phoenix, OpenTelemetry, and NAT evals.

---

## Observability trailheads

- `1_Climate_Agent_Workflow/src/configs/config.yml` already declares a `general.telemetry.tracing.phoenix` block. With the Phoenix env vars exported, every `nat run` / `nat serve` session streams OpenTelemetry traces (tool invocations, latencies, errors) into your Phoenix project.
- Check the Phoenix UI (under your `${PHOENIX_PROJECT}`) to inspect trace graphs right after running `make run_1_*` or hitting the REST endpoints.
- Later lessons layer in `nat eval`, `nat optimize`, and additional exporters, but Phoenix gives you immediate visibility today.

---

## Ready for the next video?

- [Lesson 1 README](1_Climate_Agent_Workflow/README.md): run the tool-enabled climate workflow, generate visualizations, and hit the APIs.
- Upcoming folders: deepen observability, integrate retrievers, wire evaluators, and connect the official NeMo Agent Toolkit UI.

Let’s turn that 60% demo into a production-ready climate assistant.
