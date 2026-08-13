# from crewai import Agent
# from tools import youtube_channel_tool
# from llm import ollama_llm

# blog_researchers = Agent(
    
#     role = 'blog researcher from youtbe videos',
#     goal = 'get the relavant video content for the {topic}',
#     verbose = True,
#     memory = True,
#     backstory = (
#        "expert in understanding videos in AI data science, machine learning and gen AI" 
#     ),
#     tools = [youtube_channel_tool],
#     llm=ollama_llm,
#     allow_delegation = True
# )

# blog_writer = Agent(
    
#     role = 'blog writer',
#     goal = 'narrate compelling tech storied about the video {topic} from Youtube',
#     verbose = True,
#     memory = True,
#     backstory = (
#        "with a flair for simplifying complex topics, you craft"
#        "enganing narratives that captivate and educate, bringing new"
        
#     ),
#     tools = [youtube_channel_tool],
#     llm=ollama_llm,
#     allow_delegation = False
# )

from crewai import Agent
from llm import ollama_llm


blog_researcher = Agent(
    role="AI Researcher",
    goal="Research and explain information about {topic}",
    backstory=(
        "You are an expert in AI, machine learning, "
        "data science and generative AI."
    ),
    llm=ollama_llm,
    verbose=True,
    allow_delegation=False
)


blog_writer = Agent(
    role="Technical Blog Writer",
    goal="Write a clear technical blog about {topic}",
    backstory=(
        "You are an experienced technical writer who "
        "simplifies complex technical concepts."
    ),
    llm=ollama_llm,
    verbose=True,
    allow_delegation=False
)