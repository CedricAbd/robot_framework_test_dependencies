# robot_framework_test_dependencies

## Info:
Robot Framework Test Dependencies is a lightweight desktop tool that:
1. Pulls a Robot Framework test from GitLab
2. Recursively resolves every resource, library and variables imports
3. Builds an interactive dependency graph
4. Lets you export the full list as a .txt file

## Requirements:
1. System (APT):
   - python3-tk
   - graphviz
   - libgraphviz-dev
2. Python (pip):
   - python-gitlab
   - robotframework
   - networkx
   - pygraphviz
   - matplotlib
