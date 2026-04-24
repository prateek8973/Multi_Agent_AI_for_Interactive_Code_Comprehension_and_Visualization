import os
from crewai.tools import tool


# 🔹 Pure function (used in backend)
def _list_repository_files(repo_path: str) -> list:
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files[:200]


# 🔹 Tool wrapper (used by agents)
@tool
def list_repository_files(repo_path: str) -> list:
    """
    Lists files inside a repository.
    """
    return _list_repository_files(repo_path)


# 🔹 Pure function (used in backend)
def _read_repository_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()[:8000]
    except Exception as e:
        return str(e)


# 🔹 Tool wrapper (used by agents)
@tool
def read_repository_file(file_path: str) -> str:
    """
    Reads contents of a file.
    """
    return _read_repository_file(file_path)
