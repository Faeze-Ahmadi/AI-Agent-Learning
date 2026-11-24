## My Implementation Notes

This project is based on the original [Agent-Steps](https://github.com/nilay1400/Agent-Steps) repository and was implemented as a learning exercise for my AI course.

### Environment
- OS: Windows 10
- Python: 3.12
- Package Manager: uv
- Frameworks: LangChain and LangGraph
- LLM: Qwen via Groq API

### Changes I Made
1. Set up and ran the project on Windows instead of WSL Ubuntu.
2. Modified the `.env` file path in `main.py`.
3. Changed the language model to `qwen/qwen3.8-27b`.
4. Changed the test numbers to `731137371 + 371137317`.
5. Successfully tested the agent using the `add` and `get_weather` tools.

### Result
The agent successfully called both tools and generated the final response.

This project helped me understand AI Agents, API calls, and tool calling using LangChain and LangGraph.


## Week 2. MCP Server and Custom Tools

This week, I extended the original project's MCP server by implementing two custom tools using **FastMCP**.

### 1. Privacy Guard

The `privacy_guard` tool uses Python regular expressions to detect and hide email addresses in text.

**Example:**

Input: `My email is student@gmail.com`

Output: `My email is [HIDDEN EMAIL]`

**Purpose:** Basic privacy protection before sharing text or logs.

### 2. Sampling Analyzer

The `sampling_analyzer` tool analyzes how temperature scaling changes a probability distribution and calculates its Shannon entropy.

Temperature scaling is defined as:

\(q_i = \frac{p_i^{1/T}}{\sum_j p_j^{1/T}}\)

**Example:**

Input:
- Probabilities: `[0.7, 0.2, 0.1]`
- Temperature: `2.0`

Output:
- Adjusted probabilities: `[0.5229, 0.2795, 0.1976]`
- Entropy: `1.0158`

**Purpose:** Exploring probability distributions and sampling behavior in language models.

### MCP Client Testing

I created `test_mcp.py` to connect to the MCP server through the stdio transport.

The client successfully:
- Initialized an MCP session.
- Discovered all five registered tools.
- Called `privacy_guard` and `sampling_analyzer`.
- Received the expected results from both tools.

**Run the test:**

```bash
uv run python test_mcp.py
```

The two new tools do not require Docker or an external LLM API. The existing `run_python` tool uses Docker.

**Files added or updated:** `src/basic_agent/mcp_server.py`, `test_mcp.py`, `pyproject.toml`, and `uv.lock`.