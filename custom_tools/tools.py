from composio_gemini import ComposioToolSet, App, Action
import os

toolset = ComposioToolSet(api_key=os.environ['COMPOSIO_API_KEY'])
bdr_tools = toolset.get_tools(actions=[Action.GMAIL_CREATE_EMAIL_DRAFT, Action.GMAIL_SEND_EMAIL], skip_default=True)
sales_tools = toolset.get_tools(apps=[App.EXA], skip_default=True)
