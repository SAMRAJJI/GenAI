# from crewai import Task
# from agent import blog_researcher, blog_writer
# from tools import youtube_channel_tool

# research_task = Task(
#     description=(
#         "Research the YouTube channel {youtube_channel_handle} "
#         "and find relevant machine learning and AI tutorial content. "
#         "Extract the important information that can be used for a technical blog."
#     ),
    
#     expected_output=(
#         "A comprehensive research report containing the relevant "
#         "video topics, important concepts, explanations, and useful details."
#     ),
    
#     tools=[youtube_channel_tool],
#     agent=blog_researcher
# )


# writing_task = Task(
#     description=(
#         "Using the research from the previous task, write an engaging "
#         "technical blog about the machine learning and AI content "
#         "found on the YouTube channel {youtube_channel_handle}."
#     ),
    
#     expected_output=(
#         "A clear and engaging technical blog explaining the most "
#         "important machine learning and AI concepts from the researched videos."
#     ),
    
#     agent=blog_writer,
#     async_execution=False,
#     output_file="new_blog.md"
# )

from crewai import Task
from agent import blog_researcher, blog_writer


research_task = Task(
    description=(
        "Explain what machine learning is. "
        "Give the important concepts in a simple way."
    ),
    expected_output=(
        "A clear explanation of machine learning "
        "with its important concepts."
    ),
    agent=blog_researcher
)


writing_task = Task(
    description=(
        "Using the research from the previous task, "
        "write a short technical blog about machine learning."
    ),
    expected_output=(
        "A clear and engaging technical blog about machine learning."
    ),
    agent=blog_writer,
    output_file="new_blog.md"
)