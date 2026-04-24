from fastapi import FastAPI
from crew_setup import create_crew
from graph.dependency_graph import build_dependency_graph
from tools.file_tools import _list_repository_files
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from crewai import Crew, Task, Process
from agents.analyzer import analyzer
from tools.file_tools import _read_repository_file
import urllib.parse
from tools.ast_tools import parse_code_structure, get_function_code, build_context
import subprocess
from pydantic import BaseModel
from pathlib import Path
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze_repo(repo_path: str, query: str):
    crew = create_crew(query, repo_path)
    result = crew.kickoff()
    return {"result": result}

@app.get("/graph")
def get_dependency_graph(repo_path: str):
    files = _list_repository_files(repo_path)

    G, file_map = build_dependency_graph(files)  #  CHANGE

    nodes = list(G.nodes)
    edges = [{"source": u, "target": v} for u, v in G.edges]

    return {
        "nodes": nodes,
        "edges": edges,
        "file_map": file_map  # IMPORTANT
    }

from agents.debugger import debugger
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    file_path: str


@app.post("/debug")
def debug_file(request: AnalyzeRequest):
    import urllib.parse

    decoded_path = urllib.parse.unquote(request.file_path)
    content = _read_repository_file(decoded_path)

    task = Task(
        description=f"""
        Analyze this file for:
        - Bugs
        - Logical errors
        - Edge cases
        - Performance issues

        Provide fixes with code examples.

        File:
        {content}
        """,
        expected_output="List of bugs with fixes",
        agent=debugger
    )

    crew = Crew(
        agents=[debugger],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    return {"result": str(result)}

from agents.security import security_agent

@app.post("/security")
def security_check(request: AnalyzeRequest):
    import urllib.parse

    decoded_path = urllib.parse.unquote(request.file_path)
    content = _read_repository_file(decoded_path)

    task = Task(
        description=f"""
        Analyze this file for security vulnerabilities:

        - Injection risks
        - Hardcoded secrets
        - Unsafe file handling
        - Insecure practices

        Provide severity (Low/Medium/High) and fixes.

        File:
        {content}
        """,
        expected_output="Security issues with fixes",
        agent=security_agent
    )

    crew = Crew(
        agents=[security_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    return {"result": str(result)}

@app.get("/file")
def get_file_content(file_path: str):
    # decode URL-encoded path
    decoded_path = urllib.parse.unquote(file_path)

    content = _read_repository_file(decoded_path)

    return {
        "file_path": decoded_path,
        "content": content
    } 

from pydantic import BaseModel

class AskRequest(BaseModel):
    file_path: str
    question: str


@app.post("/ask")
def ask_about_file(request: AskRequest):
    decoded_path = urllib.parse.unquote(request.file_path)
    content = _read_repository_file(decoded_path)

    task = Task(
        description=f"""
        Answer the user's question about this file.

        File content:
        {content}

        Question:
        {request.question}
        """,
        expected_output="Clear and helpful answer",
        agent=analyzer
    )

    crew = Crew(
        agents=[analyzer],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()

    return {
    "answer": result if isinstance(result, str) else str(result)
}

@app.get("/structure")
def get_structure(file_path: str):
    decoded = urllib.parse.unquote(file_path)
    content = _read_repository_file(decoded)

    structure = parse_code_structure(content)
    return structure 


class CodeRequest(BaseModel):
    code: str
    language: str  # python, js, java, cpp


EXT_MAP = {
    "python": "py",
    "js": "js",
    "javascript": "js",
    "java": "java",
    "cpp": "cpp"
}


@app.post("/sandbox")
def run_in_sandbox(req: CodeRequest):
    ext = EXT_MAP.get(req.language.lower())
    if not ext:
        return {"error": "Unsupported language"}

    # ✅ ALWAYS use this path logic (Windows-safe)
    sandbox_dir = Path("sandbox").resolve()
    sandbox_dir.mkdir(parents=True, exist_ok=True) 
    filename = f"generated.{ext}"
    filepath = sandbox_dir / filename
    print("Sandbox path:", sandbox_dir)
    # write file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(req.code)

    try:
        result = subprocess.run(
            [
                "docker", "run",
                "--rm",
                "--memory=100m",
                "--cpus=0.5",
                "--network=none",
                "-e", f"FILENAME={filename}",
                "-v", f"{sandbox_dir.as_posix()}:/app",
                "code-sandbox"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
