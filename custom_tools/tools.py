from composio_gemini import ComposioToolSet, App, Action
import os

toolset = ComposioToolSet(api_key=os.environ['COMPOSIO_API_KEY'])
bdr_tools = toolset.get_tools(actions=[Action.GMAIL_SEND_EMAIL], skip_default=True)
search_tools =  toolset.get_tools(actions=[Action.PERPLEXITYAI_PERPLEXITY_AI_SEARCH, 
                                           Action.EXA_SEARCH,
                                           Action.APOLLO_SEARCH_ACCOUNTS,
                                           Action.APOLLO_SEARCH_CONTACTS,
                                           Action.APOLLO_PEOPLE_SEARCH,
                                           Action.APOLLO_PEOPLE_ENRICHMENT], skip_default=True)