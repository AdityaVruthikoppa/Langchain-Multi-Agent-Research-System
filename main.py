from src.langchain_multi_agent_research_system.tools.tools import web_search, web_scrape

print(web_scrape.invoke("https://ai.google/research"))