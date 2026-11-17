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
