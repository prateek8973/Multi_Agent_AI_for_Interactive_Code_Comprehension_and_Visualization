import ast
from crewai.tools import tool


@tool
def extract_functions(file_content: str) -> list:
    """
    Extracts all functions from a Python file.
    """
    try:
        tree = ast.parse(file_content)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return functions

    except Exception as e:
        return [str(e)]


@tool
def extract_classes(file_content: str) -> list:
    """
    Extracts class definitions from Python code.
    """
    try:
        tree = ast.parse(file_content)
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return classes

    except Exception as e:
        return [str(e)] 
import ast


def parse_code_structure(file_content: str):
    tree = ast.parse(file_content)

    structure = {
        "functions": [],
        "classes": [],
        "imports": []
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            structure["functions"].append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "lineno": node.lineno,
                "end_lineno": getattr(node, "end_lineno", node.lineno + 5)
            })

        elif isinstance(node, ast.ClassDef):
            structure["classes"].append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": getattr(node, "end_lineno", node.lineno + 10),
                "methods": [
                    {
                        "name": n.name,
                        "lineno": n.lineno,
                        "end_lineno": getattr(n, "end_lineno", n.lineno + 5)
                    }
                    for n in node.body if isinstance(n, ast.FunctionDef)
                ]
            })

        elif isinstance(node, ast.Import):
            for n in node.names:
                structure["imports"].append(n.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                structure["imports"].append(node.module)

    return structure

def extract_code_block(file_content: str, start_line: int, end_line: int):
    lines = file_content.split("\n")

    # safety bounds
    start_line = max(1, start_line)
    end_line = min(len(lines), end_line)

    return "\n".join(lines[start_line-1:end_line])

def get_function_code(file_content, function_name):
    tree = ast.parse(file_content)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return extract_code_block(
                file_content,
                node.lineno,
                getattr(node, "end_lineno", node.lineno + 5)
            )

    return None

def build_context(file_content, question):
    structure = parse_code_structure(file_content)

    context_parts = []
    question_lower = question.lower()

    # 🔹 1. Match functions
    for func in structure["functions"]:
        if func["name"].lower() in question_lower:
            code = extract_code_block(
                file_content,
                func["lineno"],
                func["end_lineno"]
            )
            context_parts.append(f"# Function: {func['name']}\n{code}")

    # 🔹 2. Match class names
    for cls in structure["classes"]:
        if cls["name"].lower() in question_lower:
            code = extract_code_block(
                file_content,
                cls["lineno"],
                cls["end_lineno"]
            )
            context_parts.append(f"# Class: {cls['name']}\n{code}")

        # 🔹 3. Match methods inside classes
        for method in cls["methods"]:
            if method["name"].lower() in question_lower:
                code = extract_code_block(
                    file_content,
                    method["lineno"],
                    method["end_lineno"]
                )
                context_parts.append(f"# Method: {method['name']}\n{code}")

    # 🔹 4. Fallback (SMART, not full dump)
    if not context_parts:
        summary = []

        summary.append("Functions:")
        summary.extend([f["name"] for f in structure["functions"]])

        summary.append("\nClasses:")
        summary.extend([c["name"] for c in structure["classes"]])

        context_parts.append("\n".join(summary))

    return "\n\n".join(context_parts)
