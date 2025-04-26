from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from custom_agents.ai_sales_agent import sales_agent
from custom_tools.tools import bdr_tools

bdr_agent = Agent(
    name='BDR_Agent',
    instruction=f"""
    You are an AI BDR Agent from Composio that has access to an AI Sales Agent and a Gmail Tool.
    Your job is to use the AI Sales Agent to perform research (ensure it gives you a detailed breakdown of what it searched) on the candidate and then based on the detailed research draft a really good detailed hyperpersonalised outreach email attaching the link to the AI SDR Agent in it (the link will be given as input). 
    The goal should be to talk about the AI SDR Agent. Write on behalf of Soham Ganatra, CEO of Composio""",
    tools = [AgentTool(sales_agent)]+bdr_tools,
    model='gemini-2.5-pro-preview-03-25'
)