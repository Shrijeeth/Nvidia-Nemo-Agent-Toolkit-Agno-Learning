import json
from typing import Any

import requests

BASE_URL = "http://localhost:8000"


def _print_response(label: str, response: requests.Response) -> None:
    print(f"\n--- {label} ---")
    print(f"Status: {response.status_code}")
    try:
        body: Any = response.json()
        print(json.dumps(body, indent=2))
    except ValueError:
        print(response.text)


def test_generate_endpoint():
    payload = {"inputs": "Summarize the greenhouse effect in two sentences."}
    resp = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    _print_response("POST /generate", resp)


def test_chat_endpoint():
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful climate assistant."},
            {"role": "user", "content": "Explain climate vs weather in one line."},
        ],
        "stream": False,
    }
    resp = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
    _print_response("POST /chat", resp)


def test_v1_chat_completions_endpoint():
    payload = {
        "messages": [{"role": "user", "content": "Give a climate fact."}],
        "model": "climate_agent",
    }
    resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=30)
    _print_response("POST /v1/chat/completions", resp)
