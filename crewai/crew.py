# from crewai import Crew, Process
# from agent import blog_writer, blog_researcher
# from task import research_task, writing_task

# crew = Crew(
#     agents=[
#         blog_researcher,
#         blog_writer
#     ],
#     tasks=[
#         research_task,
#         writing_task
#     ],
#     process=Process.sequential,
#     memory=True,
#     verbose=True
# )
# result = crew.kickoff(
#     inputs={
#         "youtube_channel_handle": "@exampleChannel"
#     }
# )
# print(result)

from crewai import Crew, Process

from agent import blog_writer, blog_researcher
from task import research_task, writing_task


crew = Crew(
    agents=[
        blog_researcher,
        blog_writer
    ],
    tasks=[
        research_task,
        writing_task
    ],
    process=Process.sequential,
    verbose=True
)


result = crew.kickoff()

print(result)