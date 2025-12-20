# NVIDIA NeMo Agent Toolkit – Learning Sandbox

This repo captures hands-on experiments while learning the NVIDIA NeMo Agent Toolkit (NAT) with the AGNO wrapper. Each subdirectory showcases a specific workflow; the first one builds a climate-focused agent.

## Environment setup

1. Copy `.env.example` to `.env` and populate secrets such as `NVIDIA_BASE_URL` and `NVIDIA_API_KEY`.
2. Load those values into your shell using the Make-based helper:

| Shell      | Command |
|------------|---------|
| macOS / Linux | `source <(make env)` |
| PowerShell | `make env TARGET_SHELL=env-pwsh \| Invoke-Expression` |
| cmd.exe    | `for /f "delims=" %i in ('make env TARGET_SHELL=env-cmd') do %i` |

`make env` simply parses `.env` and prints the appropriate export statements for your platform.

## First NAT Workflow

[`1_First_NAT_Workflow/README.md`](1_First_NAT_Workflow/README.md) walks through the climate agent example step-by-step: how the config is structured, how the AGNO builder wires up the LLM, and how to run/serve/test it. Quick reference:

```bash
make install_dependencies   # install uv
make install_1              # uv editable install of the workflow package
make run_1_1                # example NAT run with a predefined prompt
make serve_1                # launch the FastAPI server on localhost:8000
make test_api_1             # execute integration tests (prints responses)
```

Feel free to add more learning experiments in sibling folders (e.g., `2_Advanced_Tools_Workflow`) following the same pattern.
