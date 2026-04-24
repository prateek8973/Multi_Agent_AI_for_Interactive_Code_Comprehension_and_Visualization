import os
import networkx as nx
from tools.file_tools import _read_repository_file
from tools.dependency_tools import _extract_imports


def build_dependency_graph(file_paths):
    G = nx.DiGraph()
    file_map = {}

    for file in file_paths:
        name = os.path.basename(file)
        file_map[name] = file

    for name, path in file_map.items():
        content = _read_repository_file(path)
        imports = _extract_imports(content)

        for imp in imports:
            imp_name = imp.split(".")[-1]
            possible_file = imp_name + ".py"

            if possible_file in file_map:
                G.add_edge(name, possible_file)

    return G, file_map  # 🔥 IMPORTANT
