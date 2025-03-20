import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def client(service_name: str = 'tasks', version: str = 'v1'):
    """Creates and returns an authenticated Google service client.
    
    Args:
        service_name: The name of the Google service (default: 'tasks')
        version: The API version to use (default: 'v1')
    
    Returns:
        An authenticated Google service client
        
    Raises:
        ValueError: If GOOGLE_OAUTH_TOKEN environment variable is not set
        HttpError: If there's an error building the service
    """
    token = os.getenv('GOOGLE_OAUTH_TOKEN')
    if token is None:
        raise ValueError("GOOGLE_OAUTH_TOKEN environment variable is not set")

    creds = Credentials(token=token)
    try:
        service = build(serviceName=service_name, version=version, credentials=creds)
        return service
    except HttpError as err:
        print(err)
        exit(1)


def get_tasks_service():
    """Creates and returns an authenticated Google Tasks service client."""
    return client('tasks', 'v1') 