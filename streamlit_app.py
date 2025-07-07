import streamlit as st
import pandas as pd
from google.adk.runners import Runner
from google.adk.agents import Agent
from custom_agents.ai_bdr_agent import bdr_agent
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
import nest_asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'FALSE'

APP_NAME = "agent_comparison_app"
USER_ID = "test_user_456"
SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"

session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)

bdr_agent_runner = Runner(
    agent=bdr_agent,
    app_name=APP_NAME,
    session_service=session_service
)

async def call_agent(
    runner_instance: Runner,
    agent_instance: Agent,
    session_id: str,
    query_json: str
) -> dict:
    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])
    
    final_response_content = "No final response received."
    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text

    current_session = session_service.get_session(app_name=APP_NAME,
                                                user_id=USER_ID,
                                                session_id=session_id)
    stored_output = None
    if current_session:
        stored_output = current_session.state.get(agent_instance.output_key)
        try:
            if stored_output is not None:
                stored_output = json.loads(stored_output)
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "response": final_response_content,
        "stored_output": stored_output
    }

def main():
    st.set_page_config(page_title="Outreach Agent", page_icon="🤖", layout="wide")
    st.title("Outreach Agent")

    tab1, tab2 = st.tabs(["Single Contact", "Batch Processing"])

    with tab1:
        st.header("Single Contact Processing")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
        with col2:
            company = st.text_input("Company")
            link = st.text_input("Link")

        if st.button("Generate Outreach", key="single_contact"):
            if not all([first_name, last_name, company, link]):
                st.error("Please fill in all fields")
            else:
                with st.spinner("Generating outreach..."):
                    query = f"""
                    first_name = "{first_name}"
                    last_name = "{last_name}"
                    company = "{company}"
                    link = '{link}'
                    Show me the research report as well with sources
                    """
                    
                    nest_asyncio.apply()
                    result = asyncio.run(call_agent(bdr_agent_runner, bdr_agent, SESSION_ID_TOOL_AGENT, query))
                    
                    st.subheader("Agent Response")
                    st.write(result["response"])
                    
                    if result["stored_output"]:
                        st.subheader("Additional Information")
                        st.json(result["stored_output"])

    with tab2:
        st.header("Batch Processing")
        uploaded_file = st.file_uploader("Upload CSV file", type="csv")
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            
            required_columns = ['first_name', 'last_name', 'company', 'link']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"CSV is missing required columns: {', '.join(missing_columns)}")
            else:
                if st.button("Process Batch", key="batch_process"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for index, row in df.iterrows():
                        progress = (index + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Processing {row['first_name']} {row['last_name']} ({index + 1}/{len(df)})")
                        
                        query = f"""
                        first_name = "{row['first_name']}"
                        last_name = "{row['last_name']}"
                        company = "{row['company']}"
                        link = '{row['link']}'
                        Show me the research report as well with sources
                        """
                        
                        with st.expander(f"Results for {row['first_name']} {row['last_name']}", expanded=False):
                            nest_asyncio.apply()
                            result = asyncio.run(call_agent(bdr_agent_runner, bdr_agent, SESSION_ID_TOOL_AGENT, query))
                            
                            st.write("**Agent Response:**")
                            st.write(result["response"])
                            
                            if result["stored_output"]:
                                st.write("**Additional Information:**")
                                st.json(result["stored_output"])
                    
                    progress_bar.empty()
                    status_text.text("Batch processing completed!")

if __name__ == "__main__":
    main() 