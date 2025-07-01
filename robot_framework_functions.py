from robot.api import TestSuite
import sys
from gitlab import Gitlab
from gitlab_functions import get_file_content

def get_robot_dependencies(file_content: str) -> dict:
    """
    Gets a .robot or a .resource file dependencies (resources, libraries, variables).

    Args:
        file_content (str): File text content

    Returns:
        dict: Resource, library and variables dependencies
    """
    try:
        test_suite = TestSuite.from_string(file_content)
        results = {
            "resources": [],
            "libraries": [],
            "variables": []
        }
        for imported in test_suite.resource.imports:
            match imported.type:
                case "RESOURCE":
                    results["resources"].append(imported.name)
                case "LIBRARY":
                    results["libraries"].append(imported.name)
                case "VARIABLES":
                    results["variables"].append(imported.name)
        return results
    except Exception as e:
        print(e)
        sys.exit(1)

def build_tree(
    connection: Gitlab,
    project_path: str,
    branch_name: str,
    file_path: str,
) -> dict:
    """
    Builds a tree recursively.

    Args:
        connection (Gitlab): GitLab's connection
        project_path (str): Path to a GitLab project
        branch_name (str): Name of a GitLab branch
        file_path (str): Path to the root node

    Returns:
        dict: Built tree
    """
    def _process_node(path: str) -> dict:
        """
        Processes a node.

        Args:
            path (str): Path to the node

        Returns:
            dict: Node as a dictionary
        """
        try:
            content = get_file_content(connection, project_path, branch_name, path)
            node = {"name": path, "type": "root", "children": []}
            if not content:
                return node
            if path.endswith(".robot") or path.endswith(".resource"):
                dependencies = get_robot_dependencies(content)
                for library in dependencies["libraries"]:
                    node["children"].append({"name": library, "type": "library", "children": []})
                for variable in dependencies["variables"]:
                    node["children"].append({"name": variable, "type": "variable", "children": []})
                for resource in dependencies["resources"]:
                    child_node = _process_node(resource)
                    node["children"].append({
                        "name": child_node["name"],
                        "type": "resource",
                        "children": child_node["children"]
                    })
            return node
        except Exception as e:
            print(node["name"] + str(e))
            sys.exit(1)
    return _process_node(file_path)
