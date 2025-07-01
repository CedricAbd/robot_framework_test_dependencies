from utils_functions import load_config, build_graph
from gitlab_functions import get_gitlab_connection
from robot_framework_functions import build_tree
from tkinter_functions import launch_gui

CONFIG_FILE_PATH = "config.yaml"

if __name__ == "__main__":
    print("------------------------")
    print("Loading configuration...")
    print("------------------------")
    config = load_config(CONFIG_FILE_PATH)
    print("OK: Configuration loaded")
    print("-----------------------")
    print("Connecting to GitLab...")
    print("-----------------------")
    connection = get_gitlab_connection(
        config["gitlab_url"],
        config["private_token"]   
    )
    print("OK: Connected to GitLab")
    print("-----------------------------")
    print("Starting tree construction...")
    print("-----------------------------")
    tree = build_tree(
        connection,
        config["project_path"],
        config["branch_name"],
        config["file_path"]
    )
    print("OK: Tree successfully built")
    print("-------------------------------------")
    print("Launching graphical user interface...")
    print("-------------------------------------")
    launch_gui(build_graph(tree))
