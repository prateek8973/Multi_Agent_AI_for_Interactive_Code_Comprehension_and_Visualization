from crewai import Agent
from llm_config import llm

teacher = Agent(
    role="Code Teacher",
    goal="Explain code in a beginner-friendly way",
    backstory="CS professor who teaches using simple analogies",
    llm=llm,
    verbose=True,
)
