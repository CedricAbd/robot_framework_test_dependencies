from gitlab import Gitlab
import sys
import base64

def get_gitlab_connection(
    gitlab_url: str,
    private_token: str,
) -> Gitlab:
    """
    Gets a connection to a Gitlab repository.

    Args:
        gitlab_url (str): GitLab's URL
        private_token (str): User's GitLab private token

    Returns:
        Gitlab: Connection to a GitLab repository
    """
    try:
        connection = Gitlab(gitlab_url, private_token)
        connection.auth()
        return connection
    except Exception as e:
        print(e)
        sys.exit(1)

def get_file_content(
    connection: Gitlab,
    project_path: str,
    branch_name: str,
    file_path: str
) -> str:
    """
    Gets a GitLab file text content.

    Args:
        connection (Gitlab): GitLab's connection
        project_path (str): Path to a GitLab project
        branch_name (str): Name of a GitLab branch
        file_path (str): Path to the file to get the content from

    Returns:
        str: File raw content
    """
    try:
        project = connection.projects.get(project_path)
        file = project.files.get(file_path=file_path, ref=branch_name)
        return base64.b64decode(file.content).decode('utf-8')
    except Exception as e:
        print(file_path + str(e))
        return ""
