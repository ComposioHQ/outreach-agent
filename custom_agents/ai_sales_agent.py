
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from custom_tools.tools import sales_tools
sales_agent = Agent(
    name='Sales_Agent',
    instruction="""
    # | Tool or action | Purpose | Typical reasoning the agent performs
1 | Enrich contact & company (LinkedIn + Google) | Get canonical profile URLs and website — groundwork for all later scrapes. | “Are there multiple John Lees at Gong? Which one matches title / city / industry?”
2 | Scrape contact LinkedIn profile | Capture headline, about, employment history, skills, wins. | Filters for achievements (ARR targets, President’s Club, etc.)
3 | Scrape recent contact LinkedIn posts | Surface opinions, priorities, pain points. | Retains only posts that show growth pains, hiring asks, tech changes.
4 | Scrape company LinkedIn profile | Grab size, funding, tagline, industry tags. | Cross-checks with website “About” to avoid stale data.
5 | Scrape company LinkedIn posts | Spot launches, funding celebrates, AI initiatives. | Timestamps each post for “freshness” scoring.
6 | Company website crawl | Collect product pages, pricing, blog RSS, careers page. | If multiple sub-domains, picks marketing site first.
7 | Website vision analysis | Screenshot → GPT-Vision summary of banners & CTAs. | Detects PLG cues (“Start free”, “Book demo”) to tailor outreach hook.
8 | Google search (expansion / growth / raise / AI) | Find press & news outside LinkedIn. | Builds advanced query with “site:news & (raise OR expansion)”.
9 | Select best search result | Uses title + snippet relevance score, discards paywalled & ancient articles. |
10 | Scrape chosen article | Extract facts (amount raised, regional office opened, product GA date). |
11 | Google search (product releases) | Second thematic pass focused on launches / roadmap. |
12 | Scrape matching article | Same as #10, adds to RecentEvents. |
13 | Google search (customers) | Seeks lists of marquee customers, case-studies. |
14 | Scrape result | Builds “Notable customers” list with proof URLs. |
15 | LinkedIn Jobs scraper | Fetches live vacancies; groups by function (Sales, Eng, Ops). | Infers GTM focus: hiring 10+ AEs → growth push.
16 | Apollo tech-stack lookup & categoriser | Pulls raw tech list → LLM buckets into CRM, Analytics, DevOps, etc. | Highlights overlaps with your offer (e.g., uses HubSpot & Salesforce).
17 | Knowledge-base similarity search | (Not counted in cost calc but runs) - Retrieves top-3 “look-alike” customers your company has already served. |
    Don't give up use different search tactics.
    Return all the info above as a list in your report and the sources of the info.

    Use all the available tools
    """,
    tools=sales_tools+[google_search],
    model='gemini-2.5-pro-preview-03-25'
)