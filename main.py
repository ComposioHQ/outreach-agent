from google.adk.runners import Runner
from google.adk.agents import Agent
from custom_agents.ai_bdr_agent import bdr_agent
from custom_agents.ai_sales_agent import sales_agent
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
import nest_asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_GENAI_USE_VERTEXAI']='FALSE'


APP_NAME = "agent_comparison_app"
USER_ID = "test_user_456"
SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"
SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz"

session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)

bdr_agent_runner = Runner(
    agent=bdr_agent,
    app_name=APP_NAME,
    session_service=session_service
)

async def call_agent_and_print(
    runner_instance: Runner,
    agent_instance: Agent,
    session_id: str,
    query_json: str
):
    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")

    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")

    current_session = session_service.get_session(app_name=APP_NAME,
                                                  user_id=USER_ID,
                                                  session_id=session_id)
    stored_output = current_session.state.get(agent_instance.output_key)

    # Pretty print if the stored output looks like JSON (likely from output_schema)
    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    try:
        # Attempt to parse and pretty print if it's JSON
        parsed_output = json.loads(stored_output)
        print(json.dumps(parsed_output, indent=2))
    except (json.JSONDecodeError, TypeError):
         # Otherwise, print as string
        print(stored_output)
    print("-" * 30)

async def main():
    print("--- Testing Agent with Tool ---")
    await call_agent_and_print(bdr_agent_runner, bdr_agent, SESSION_ID_TOOL_AGENT, """
    first_name = "Norman"
    last_name = "Osborn"
    company = "Oscorp"
    link = 'example.com'
    Show me the research report as well with sources
    """)

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
