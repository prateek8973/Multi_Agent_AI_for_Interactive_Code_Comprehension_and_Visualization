from crewai import Agent
from llm_config import llm
planner = Agent(
    role="Codebase Planner",
    goal="Plan how to explore the repository to answer user questions",
    backstory=(
        "You are a senior software architect skilled at navigating large repositories."
    ),
    llm=llm,
    max_iterations=3,
    verbose=True,
)
