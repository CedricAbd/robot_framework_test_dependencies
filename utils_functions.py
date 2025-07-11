import yaml
import sys
import posixpath
import networkx as nx

def load_config(yaml_path: str) -> dict:
    """
    Loads configuration from a yaml file.

    Args:
        yaml_path (str): Path to the yaml file to load

    Returns:
        dict: Loaded configuration as a dictionary 
    """
    try:
        with open(yaml_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(e)
        sys.exit(1)

def resolve_relative_paths(current_node_path: str, imported_path: str) -> str:
    """
    Resolves a relative or absolute import path.

    Args:
        current_node_path (str): Path to the current visited node
        imported_path (str): Path of the import (absolute or relative)

    Returns:
        str: Resolved path
    """
    base_dir = posixpath.dirname(current_node_path)
    joined_path = posixpath.join(base_dir, imported_path)
    normalized_path = posixpath.normpath(joined_path)
    return normalized_path.lstrip("./")

def build_graph(node: dict, graph: nx.DiGraph = None) -> nx.DiGraph:
    """
    Builds a networkx graph recursively.

    Args:
        node (dict): Node to start from
        graph (nx.DiGraph): Graph to populate

    Returns:
        nx.DiGraph: Built networkx graph
    """
    try:
        if graph is None:
            graph = nx.DiGraph()
        node_name = node["name"]
        graph.add_node(node_name, type=node["type"])
        for child in node.get("children", []):
            child_name = child["name"]
            graph.add_node(child_name, type=child["type"])
            graph.add_edge(node_name, child_name)
            build_graph(child, graph)
        return graph
    except Exception as e:
        print(node["name"] + str(e))
        sys.exit(1)
