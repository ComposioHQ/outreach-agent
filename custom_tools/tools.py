from composio_gemini import ComposioToolSet, App, Action
import os

toolset = ComposioToolSet(api_key=os.environ['COMPOSIO_API_KEY'])
bdr_tools = toolset.get_tools(apps=[App.GMAIL], skip_default=True)
sales_tools = toolset.get_tools(apps=[App.EXA, App.WEBTOOL], skip_default=True)
