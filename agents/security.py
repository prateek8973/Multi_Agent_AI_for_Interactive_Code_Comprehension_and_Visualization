from crewai import Agent
from llm_config import llm

security_agent = Agent(
    role="Security Auditor",
    goal="Detect vulnerabilities in code",
    backstory="Cybersecurity expert specializing in code audits",
    llm=llm,
    verbose=True,
)
