import ast
from crewai.tools import tool


def _extract_imports(file_content: str) -> list:
    
    import ast
    imports = []
    try:
        tree = ast.parse(file_content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return list(set(imports))

    except Exception as e:
        return [str(e)]


@tool
def extract_imports(file_content: str) -> list:
    """
    Extract all import statements from Python code.
    """
    return _extract_imports(file_content)
