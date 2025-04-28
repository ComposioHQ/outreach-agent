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
import argparse
from dotenv import load_dotenv
from typing import Optional, Dict, Any, TYPE_CHECKING
import csv

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

# Add conditional import for Session for type hinting
if TYPE_CHECKING:
    from google.adk.sessions import Session

async def call_agent_and_print(
    runner_instance: Runner,
    agent_instance: Agent,
    session_id: str,
    query_json: str
) -> None:
    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")

    user_content: types.Content = types.Content(role='user', parts=[types.Part(text=query_json)])

    final_response_content: str = "No final response received."
    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")

    current_session: Optional[Session] = session_service.get_session(app_name=APP_NAME,
                                                  user_id=USER_ID,
                                                  session_id=session_id)
    if current_session:
        stored_output: Optional[Any] = current_session.state.get(agent_instance.output_key)
        print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
        try:
            if stored_output is not None:
                parsed_output: Dict[str, Any] = json.loads(stored_output)
                print(json.dumps(parsed_output, indent=2))
            else:
                print("None")
        except (json.JSONDecodeError, TypeError):
             # Otherwise, print as string
            print(stored_output)
        print("-" * 30)
    else:
        print(f"--- Session {session_id} not found ---")

async def main() -> None:
    # Ask user if they want to use a CSV file
    use_csv = input("Do you want to run with a CSV file? (y/n): ")
    if use_csv.strip().lower().startswith('y'):
        csv_path = input("Enter CSV file path: ")
        try:
            with open(csv_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    first_name = row.get('first_name')
                    last_name = row.get('last_name')
                    company = row.get('company')
                    link = row.get('link')
                    if not all([first_name, last_name, company, link]):
                        print(f"Skipping row with missing fields: {row}")
                        continue

                    # Construct query for this row
                    query = f"""
    first_name = "{first_name}"
    last_name = "{last_name}"
    company = "{company}"
    link = '{link}'
    Show me the research report as well with sources
    """
                    print(f"\n--- Running BDR Agent for {first_name} {last_name} at {company} ---")
                    await call_agent_and_print(bdr_agent_runner, bdr_agent, SESSION_ID_TOOL_AGENT, query)
        except FileNotFoundError:
            print("CSV file not found at", csv_path)
        except Exception as e:
            print("Error processing CSV:", e)
        return

    # --- Argument Parsing (Optional) ---
    parser = argparse.ArgumentParser(description='Run the BDR agent. Provide all contact arguments or none to be prompted interactively.')
    # Make arguments optional (remove required=True)
    parser.add_argument('--first-name', type=str, help='First name of the contact.')
    parser.add_argument('--last-name', type=str, help='Last name of the contact.')
    parser.add_argument('--company', type=str, help='Company name of the contact.')
    parser.add_argument('--link', type=str, help='Link to include in the outreach.')

    args = parser.parse_args()

    # --- Determine Input Method ---
    # Check if all required args were provided via command line
    if args.first_name and args.last_name and args.company and args.link:
        print("Using command-line arguments.")
        first_name = args.first_name
        last_name = args.last_name
        company = args.company
        link = args.link
    else:
        # --- Interactive Input ---
        print("Command-line arguments incomplete or missing. Please enter the contact details interactively:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        company = input("Company: ")
        link = input("Link to include: ")

        # --- Validate Input (Basic) ---
        if not all([first_name, last_name, company, link]):
            print("Error: All fields (First Name, Last Name, Company, Link) are required.")
            return # Exit if any field is empty

    # --- Construct Query ---
    query = f"""
    first_name = "{first_name}"
    last_name = "{last_name}"
    company and role = "{company}"
    link = '{link}'
    Show me the research report as well with sources
    """

    print(f"\n--- Running BDR Agent for {first_name} {last_name} at {company} ---")

    # --- Call Agent ---
    await call_agent_and_print(bdr_agent_runner, bdr_agent, SESSION_ID_TOOL_AGENT, query)


if __name__ == "__main__":
    # Consider adding a try/except block around main() for cleaner exit on KeyboardInterrupt
    try:
        nest_asyncio.apply()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExecution cancelled by user.")
