# NVIDIA NeMo Agent Toolkit – Learning Journey

Welcome! This repo tracks a hands-on course for building **enterprise-ready agents** with NVIDIA’s open-source NeMo Agent Toolkit (NAT). You’ll go from a fragile demo to production-grade workflows that are observable, deployable, and easy to iterate on.

The material is inspired by NVIDIA & DeepLearning.AI’s curriculum (taught by Brian McBrayer) and focuses on solving the classic AI Agents Production Problems:

- **Observability:** trace tool calls, model choices, and performance hotspots via OpenTelemetry.
- **Evaluation & optimization:** run disciplined evals, catch regressions, and tune agents automatically.
- **Deployment:** package agent workflows as APIs with auth, rate limits, and CI/CD-friendly configs.

Each folder in this repo represents a milestone in that journey, starting with a climate-analysis agent that grows from a single LLM call into a multi-agent, instrumented system.

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

1. Copy `.env.example` → `.env` and fill in secrets (`NVIDIA_BASE_URL`, `NVIDIA_API_KEY`, etc.).
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
| `1_First_NAT_Workflow/` | Build & serve a minimal climate agent (LLM-only) |
| `scripts/` | Utility helpers (env management, etc.) |
| `Makefile` | Convenience targets: install, validate, run, serve, test |

Future lessons (e.g., `2_Tools_Workflow`, `3_MultiAgent_Workflow`) will incrementally add tool calling, observability plumbing, evaluation suites, optimizers, and UI integrations.

---

## Quickstart commands (from repo root)

```bash
make install_dependencies   # install uv
make install_1              # uv editable install of the first workflow
make validate_1             # nat validate --config_file ...
make run_1_1                # ask the workflow a curated climate prompt
make serve_1                # expose FastAPI on localhost:8000
make test_api_1             # hit /generate, /chat, /v1/chat/completions and print responses
```

Need to see API output? Run `make serve_1` in one terminal and `make test_api_1` (or the curl examples in the workflow README) in another. Observability + eval tooling arrives in later lessons when we wire up Phoenix, OpenTelemetry, and NAT evals.

---

## Ready for the next video?

- [Lesson 1 README](1_First_NAT_Workflow/README.md): run your first NAT agent and serve it.
- Upcoming folders: add tools, integrate retrievers, inspect telemetry, plug in evaluators, and connect the official NeMo Agent Toolkit UI.

Let’s turn that 60% demo into a production-ready climate assistant.
