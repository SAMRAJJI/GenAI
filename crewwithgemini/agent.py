# from crewai import Agent
# from tools import tool
# from dotenv import load_dotenv
# import os
# load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(
#     model ="gemini-1.5-flash",
#     verbose= True,
#     temperature = 0.5,
#     google_api_key = os.getenv("google_api_key") 
# )

# news_researcher = Agent(
#     role ="senior researcher",
#     goal = " uncover ground breaking a technologies in {topic}",
#     verbose = True,
#     memory = True,
#     backstory = ("Driven by curiosity , you're at the forefront of"
#                  "innovation eager to explore and share knowledge that could change"
#                  "the world"
#                  ),
#     tools = [tool],
#     llm = llm,
#     allow_delegation = True
# )
import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GOOGLE_API_KEY")

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=api_key,
    temperature=0.5
)

news_researcher = Agent(
    role="senior researcher",
    goal="uncover groundbreaking technologies in {topic}",
    backstory=(
        "Driven by curiosity, you're at the forefront of "
        "innovation, eager to explore and share knowledge."
    ),
    verbose=True,
    memory=True,
    llm=llm
)