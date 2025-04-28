from composio_gemini import ComposioToolSet, App, Action
import os

toolset = ComposioToolSet(api_key=os.environ['COMPOSIO_API_KEY'])
bdr_tools = toolset.get_tools(actions=[Action.GMAIL_CREATE_EMAIL_DRAFT], skip_default=True)
sales_tools = toolset.get_tools(actions=[Action.EXA_GET_CONTENTS_ACTION], skip_default=True)
search_tools =  toolset.get_tools(actions=[Action.PERPLEXITYAI_PERPLEXITY_AI_SEARCH], skip_default=True)