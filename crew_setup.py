from crewai import Crew, Task, Process
from agents.planner import planner
from agents.explorer import explorer
from agents.analyzer import analyzer
from agents.summarizer import summarizer
from agents.debugger import debugger
from agents.security import security_agent
from agents.teacher import teacher

def create_crew(query, repo_path):

    planning = Task(
        description=f"""
        Plan how to analyze this repository.

        Query: {query}
        Repo: {repo_path}
        """,
        expected_output="Step-by-step investigation plan",
        agent=planner
    )

    exploration = Task(
        description=f"""
        Explore repository and find relevant files.

        Query: {query}
        Repo: {repo_path}
        """,
        expected_output="Relevant file paths",
        agent=explorer,
        context=[planning]
    )

    analysis = Task(
        description=f"""
        Analyze the selected files deeply.

        Query: {query}
        """,
        expected_output="Detailed system explanation",
        agent=analyzer,
        context=[exploration]
    )

    summarization = Task(
        description="Summarize the repository structure and key components",
        expected_output="Clear structured summary",
        agent=summarizer,
        context=[analysis]
    )

    debugging = Task(
        description="Find bugs and suggest fixes",
        expected_output="List of issues with fixes",
        agent=debugger,
        context=[analysis]
    )

    security = Task(
        description="Find security vulnerabilities",
        expected_output="Security issues with severity",
        agent=security_agent,
        context=[analysis]
    )

    teaching = Task(
        description="Explain the code in a beginner-friendly way",
        expected_output="Simple explanation with examples",
        agent=teacher,
        context=[analysis]
    )

    crew = Crew(
        agents=[
            planner, explorer, analyzer,
            summarizer, debugger,
            security_agent, teacher
        ],
        tasks=[
            planning, exploration, analysis,
            summarization, debugging,
            security, teaching
        ],
        process=Process.sequential,
        verbose=True
    )

    return crew