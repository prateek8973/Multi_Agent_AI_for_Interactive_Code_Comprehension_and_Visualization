from crewai import Agent
from llm_config import llm


explorer = Agent(
    role="Repository Explorer",
    goal="Locate relevant files in the repository",
    backstory="Expert at quickly locating code files relevant to a question.",   #  ADD HERE TOO
    llm=llm,
    max_iterations=3,
    verbose=True,
)
