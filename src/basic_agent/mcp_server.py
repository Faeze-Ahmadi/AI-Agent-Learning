from __future__ import annotations

import subprocess
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

import json
from pathlib import Path
from uuid import uuid4

OUTPUTS = Path("outputs")


def clip(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    OUTPUTS.mkdir(exist_ok=True)
    path = OUTPUTS / f"{uuid4().hex}.txt"
    path.write_text(text)
    return text[:limit] + f"\n... [truncated: full output in {path}]"


mcp = FastMCP("basic-agent-tools")


@mcp.tool()
def add(
    a: Annotated[int, Field(description="First integer to add")],
    b: Annotated[int, Field(description="Second integer to add")],
) -> int:
    """Add two integers exactly. Use this for arithmetic instead of estimating."""
    return a + b


@mcp.tool()
def get_weather(
    city: Annotated[str, Field(description="City name, e.g. Paris")]
) -> str:
    """Get the current weather for a city. This is a stub for class use."""
    return "sunny, 22°C"


@mcp.tool()
def run_python(
    code: Annotated[str, Field(description="Short Python code to execute")]
) -> str:
    """Execute short Python code in an isolated Docker sandbox.

    Use ONLY for nontrivial computation or data transformation.
    Do NOT use for simple addition; use the add tool.
    The sandbox has no network, a 5-8 second timeout, and 128 MB memory.
    """
    cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "128m",
        "--cpus", "0.5",
        "--pids-limit", "64",
        "--read-only",
        "--tmpfs", "/tmp:rw,size=16m,noexec,nosuid",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--user", "65534:65534",
        "python:3.12-slim",
        "python", "-I", "-c", code,
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except FileNotFoundError:
        return "ERROR: docker not found. Sandbox unavailable."
    except subprocess.TimeoutExpired:
        return "ERROR: sandbox timed out after 8 seconds."
    output = (proc.stdout or "") + (proc.stderr or "")
    return f"exit={proc.returncode}\n{clip(output)}"


@mcp.tool()
def privacy_guard(text: str) -> str:
    """Hide email addresses in a text before sharing it."""
    import re
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    cleaned_text = re.sub(
        email_pattern,
        "[HIDDEN EMAIL]",
        text
    )
    return cleaned_text


@mcp.tool()
def sampling_analyzer(
    probabilities: list[float],
    temperature: float = 1.0
) -> dict:
    """Analyze how temperature changes sampling probabilities."""
    import math
    if not probabilities or any(p < 0 for p in probabilities):
        return {"error": "Probabilities must be non-negative."}
    if temperature <= 0:
        return {"error": "Temperature must be positive."}
    total = sum(probabilities)
    if total == 0:
        return {"error": "Sum of probabilities cannot be zero."}

    normalized = [p / total for p in probabilities]
    weights = [p ** (1 / temperature) for p in normalized]
    weight_sum = sum(weights)
    adjusted = [w / weight_sum for w in weights]
    entropy = -sum(
        p * math.log(p) for p in adjusted if p > 0
    )
    return {
        "original": normalized,
        "temperature": temperature,
        "adjusted": [round(p, 4) for p in adjusted],
        "entropy": round(entropy, 4)
    }

if __name__ == "__main__":
    mcp.run()
