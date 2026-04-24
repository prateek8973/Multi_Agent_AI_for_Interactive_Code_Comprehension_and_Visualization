from crewai import Agent
from llm_config import llm

debugger = Agent(
    role="Code Debugger",
    goal="Find bugs and suggest fixes",
    backstory="Expert in debugging and improving code quality",
    llm=llm,
    verbose=True,
)
