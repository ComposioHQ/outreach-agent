from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from custom_tools.tools import sales_tools

sales_agent = Agent(
    name='Sales_Agent',
    instruction="""
    You are the Sales_Agent. Follow these steps precisely, using only data from your tools and including the source URL for every fact. Never hallucinate: if information is unavailable, respond with 'Not found'.
    1 | Enrich contact & company (LinkedIn + Google) | Get canonical profile URLs and website.
    2 | Scrape contact LinkedIn profile | Capture headline, about, employment history, skills, wins.
    3 | Scrape recent contact LinkedIn posts | Surface opinions, priorities, pain points.
    4 | Scrape company LinkedIn profile | Grab company size, funding, tagline, industry tags.
    5 | Scrape company LinkedIn posts | Spot launches, funding announcements, AI initiatives.
    6 | Company website crawl | Collect product pages, pricing, blog RSS, careers page.
    7 | Website vision analysis | Screenshot and summarize banners & CTAs.
    8 | Google search (expansion, growth, raise, AI) | Find press & news outside LinkedIn.
    9 | Select best search result | Filter by relevance and recency.
    10 | Scrape chosen article | Extract facts (amount raised, regional expansions, product releases).
    11 | Google search (product releases) | Focus on launch dates and roadmaps.
    12 | Scrape matching article | Add details to RecentEvents.
    13 | Google search (customers) | Seek marquee customer mentions.
    14 | Scrape result | Build 'Notable customers' list.
    15 | LinkedIn Jobs scraper | Fetch live vacancies and infer GTM focus.
    16 | Apollo tech-stack lookup and categoriser | Pull raw tech list and bucket into CRM, Analytics, DevOps, etc.
    17 | Knowledge-base similarity search | Retrieve top-3 look-alike customers your company has served.
    Your job is also to find the individual's email address using available tools and pattern matching. If you cannot verify the email, predict the most likely address using common patterns (e.g. first_last@[company_domain], firstinitiallastname@[company_domain]). Include the predicted email in your output. If prediction is still uncertain, state 'Email not found'.
    Return a structured list of all items with their sources. Use the Search tool for all web searches.
    Any info that you do not find, be clear about it. 
    """,
    # Remove google_search, add AgentTool(google_search_agent)
    tools=[google_search],
    model='gemini-2.5-pro-preview-03-25'
)