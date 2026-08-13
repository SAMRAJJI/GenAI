from crewai import Task
from tools import tool
from agent import news_researcher
research_task = Task(
    description = ("identify the next big trend in {topic}"
    "its market opportunity and potential risks"
    "your final report should clearly articulate the key points"
    ),
    expected_output = "a comprehensive 2 paragraphs long report on the latest AI trend",
    tools = [tool],
    agent =news_researcher,
    async_execution = False,
    output_file = 'new-blog-post.md'
)