from crewai import Agent
from llm_config import llm

summarizer = Agent(
    role="Code Summarizer",
    goal="Summarize repository structure and logic clearly",
    backstory="Expert at simplifying large codebases for developers",
    llm=llm,
    verbose=True,
)
