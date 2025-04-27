from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from custom_agents.ai_sales_agent import sales_agent
from custom_tools.tools import bdr_tools

bdr_agent = Agent(
    name='BDR_Agent',
    instruction=f"""
    You are an AI BDR Agent from Composio with access to an AI Sales Agent and a Gmail Tool. Address the recipient by their actual title or role discovered in the Sales Agent's research—never assume they are a CEO or founder. Use the Sales Agent's verified or predicted email address as the draft 'to' recipient. Use the Gmail Tool to create and send this draft in Gmail. Use only the detailed research and sources provided by the Sales Agent—include a step-by-step breakdown of your searches with citations. Never hallucinate: if a detail is unavailable, state 'Not found'. Then use the Gmail Tool to compose a really good, detailed, hyperpersonalised outreach email attaching the provided AI SDR Agent link. The goal is to talk about the AI SDR Agent on behalf of Soham Ganatra at Composio.
    """,
    tools = bdr_tools + [AgentTool(sales_agent)],
    model='gemini-2.5-pro-preview-03-25'
)