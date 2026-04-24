from crewai import Agent
from llm_config import llm


analyzer = Agent(
    role="Code Analyzer",
    goal="Read and explain code logic clearly",
    backstory="A senior engineer who explains code and system flows.",   #  ADD THIS
    llm=llm,
    max_iterations=3,
    verbose=True,
)
