from dotenv import load_dotenv
load_dotenv()
import os

os.environ['SERPER_API_KEY'] = os.getenv('serper_api_key')

from crewai_tools import SerperDevTool

tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=2,
)

print(tool.run(search_query="ChatGPT"))

