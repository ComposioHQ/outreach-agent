# AI SDR

## Overview
This project demonstrates an outreach automation workflow using Google ADK and Composio Gemini. It features two main AI agents:

- **BDR Agent**: Performs research on a candidate and company, then drafts a hyper-personalized outreach email using the research and Gmail tools.
- **Sales Agent**: Gathers detailed information about a contact and company using web, LinkedIn, and Google search tools, returning a comprehensive research report with sources.

The agents are orchestrated in a test script (`main.py`) that sends a sample query and prints the results.

---

## Codebase Structure

```
.
├── main.py                  # Entrypoint script to run agent workflows
├── requirements.txt         # Python dependencies
├── custom_agents/
│   ├── ai_bdr_agent.py      # BDR Agent definition
│   └── ai_sales_agent.py    # Sales Agent definition
├── custom_tools/
│   └── tools.py             # Custom tool definitions for agents
```

### Key Components
- **main.py**: Sets up the session, initializes agents, and runs a test query. Handles printing and pretty-printing of agent responses and session state.
- **custom_agents/ai_bdr_agent.py**: Defines the BDR Agent, which uses the Sales Agent and Gmail tool to perform research and draft emails.
- **custom_agents/ai_sales_agent.py**: Defines the Sales Agent, which uses a variety of tools to gather and report on contact and company data.
- **custom_tools/tools.py**: Configures toolsets for the agents using Composio Gemini, including Gmail, EXA, and WebTool integrations.

---

## Setup Instructions

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies** (use Python 3.10):

```sh
pip3.10 install -r requirements.txt
```

3. **Set up environment variables**:
   - Create a `.env` file in the project root with the following content:

```
COMPOSIO_API_KEY=your_composio_api_key_here
```

> The script also sets `GOOGLE_GENAI_USE_VERTEXAI=FALSE` internally, so you do not need to set this manually.

4. **Run the script**:

```sh
python3.10 main.py
```

---

## How It Works
- The script loads environment variables and sets up a session using Google ADK's in-memory session service.
- It initializes the BDR Agent (which can call the Sales Agent and use Gmail) and the Sales Agent (which uses web and LinkedIn tools).
- The `main()` function sends a sample query (with contact and company info) to the BDR Agent.
- The BDR Agent performs research (via the Sales Agent), drafts an outreach email, and the script prints the results and session state.

---

## For Developers
- To add or modify agent logic, edit the files in `custom_agents/`.
- To add or configure tools, edit `custom_tools/tools.py`.
- The code is modular and can be extended with new agents or tools as needed.
- The agents use Google ADK's async runner and session management for scalable, stateful interactions.

---

## Requirements
- Python 3.10+
- API key for Composio Gemini (see https://composio.dev/ for details)

---

