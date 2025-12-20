# First NAT Workflow (Climate Agent)

This module is a guided learning exercise for the NVIDIA NeMo Agent Toolkit (NAT). It shows how to wire the AGNO builder, configure an LLM, and expose the workflow through the CLI and FastAPI surface.

## Learning objectives

- Understand how NAT functions are declared (`climate_agent_function.py`).
- See how configs describe LLMs/tools (`src/configs/config.yml`).
- Practice running NAT both via CLI (`nat run`) and service (`nat serve`).
- Capture API interactions with lightweight integration tests.

## Prerequisites

From the repo root:

```bash
make install_dependencies
make install_1
```

Ensure `.env` is populated and loaded (see root README for details).

## Workflow anatomy

| Component | Purpose |
|-----------|---------|
| `pyproject.toml` | Defines the package and entry-point used by `nat` |
| `src/climate_agent/climate_agent_function.py` | Implements the AGNO-based function |
| `src/configs/config.yml` | Declares the workflow + LLM references |
| `tests/integration_tests/test_api.py` | Exercises HTTP endpoints and prints responses |

## Running the workflow

```bash
make run_1_1  # sample question 1
make run_1_2  # sample question 2
make run_1_3  # sample question 3
make serve_1  # start FastAPI server (required for integration tests)
```

## Integration tests

The tests hit a running server on `localhost:8000` and print full responses:

```bash
make test_api_1
```

## Configuration

- Workflow entry point: `climate_agent_function` defined in `src/climate_agent`.
- Primary config: `src/configs/config.yml`. Adjust LLM/tool references or prompts to observe changes.

Feel free to duplicate this folder to create additional learning modules (e.g., add tools, streaming, or multi-agent orchestrations).
