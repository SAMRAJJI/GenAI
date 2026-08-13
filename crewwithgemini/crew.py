from crewai import Crew, Process
from agent import news_researcher
from task import research_task
crew = Crew(
    agents= [news_researcher],
    tasks= [research_task],
    process= Process.sequential
)

res = crew.kickoff( inputs={"topic": "Artificial Intelligence"})
print(res)