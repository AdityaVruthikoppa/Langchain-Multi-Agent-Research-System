from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.langchain_multi_agent_research_system.tools.tools import web_search, web_scrape
from dotenv import load_dotenv

load_dotenv()
model=ChatOpenRouter(model="nvidia/nemotron-3-ultra-550b-a55b:free",temperature=0)

#agent for web search
def create_web_search_agent():
   return create_agent(
        model=model,
        tools=[web_search],
        
    )
# agent for web scrape
def create_web_scrape_agent():
    return create_agent(
        model=model,
        tools=[web_scrape],
        
    )   
#writer prompt for the agents
writer_prompt = ChatPromptTemplate.from_messages([
       ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Report:
{research}

Structure the report as:
- Introduction
-key Findings (Minimum 3 well-researched points)
-Conclusion
-Suggested References (Provide at least 3 references with URLs)

Be detailed and provide in-depth analysis. Use credible sources and ensure the information is accurate and up-to-date. Avoid plagiarism and ensure the content is original. Use proper citations for any references used. The report should be well-organized, with clear headings and subheadings for each section. Ensure that the language is professional and suitable for an academic or research audience. The report should be comprehensive, covering all aspects of the topic, and should provide valuable insights and recommendations based on the research conducted."""),


])
writer_chain=writer_prompt|model|StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | model | StrOutputParser()