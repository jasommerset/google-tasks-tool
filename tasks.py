import os
import sys
import json
from auth import get_tasks_service

async def list_tasklists():
    """List all task lists."""
    service = get_tasks_service()
    try:
        results = service.tasklists().list().execute()
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

async def create_tasklist():
    """Create a new task list."""
    title = os.getenv('TITLE')
    if not title:
        print("Error: TITLE environment variable not set")
        sys.exit(1)

    service = get_tasks_service()
    try:
        result = service.tasklists().insert(body={'title': title}).execute()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

async def list_tasks():
    """List tasks in a task list."""
    tasklist_id = os.getenv('TASKLIST_ID')
    if not tasklist_id:
        print("Error: TASKLIST_ID environment variable not set")
        sys.exit(1)

    service = get_tasks_service()
    try:
        results = service.tasks().list(tasklist=tasklist_id).execute()
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

async def create_task():
    """Create a new task."""
    tasklist_id = os.getenv('TASKLIST_ID')
    title = os.getenv('TITLE')
    notes = os.getenv('NOTES')  # Optional
    parent = os.getenv('PARENT_ID')  # Optional
    previous = os.getenv('PREVIOUS_ID')  # Optional

    if not tasklist_id or not title:
        print("Error: TASKLIST_ID and TITLE environment variables must be set")
        sys.exit(1)

    service = get_tasks_service()
    try:
        body = {'title': title}
        if notes:
            body['notes'] = notes

        result = service.tasks().insert(
            tasklist=tasklist_id,
            parent=parent if parent else None,
            previous=previous if previous else None,
            body=body
        ).execute()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

async def update_task():
    """Update an existing task."""
    tasklist_id = os.getenv('TASKLIST_ID')
    task_id = os.getenv('TASK_ID')
    title = os.getenv('TITLE')
    notes = os.getenv('NOTES')  # Optional
    status = os.getenv('STATUS')  # Optional

    if not all([tasklist_id, task_id, title]):
        print("Error: TASKLIST_ID, TASK_ID, and TITLE environment variables must be set")
        sys.exit(1)

    service = get_tasks_service()
    try:
        body = {'title': title}
        if notes:
            body['notes'] = notes
        if status:
            body['status'] = status

        result = service.tasks().patch(
            tasklist=tasklist_id,
            task=task_id,
            body=body
        ).execute()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

async def move_task():
    """Move a task to a new position."""
    tasklist_id = os.getenv('TASKLIST_ID')
    task_id = os.getenv('TASK_ID')
    parent = os.getenv('PARENT_ID')  # Optional
    previous = os.getenv('PREVIOUS_ID')  # Optional

    if not tasklist_id or not task_id:
        print("Error: TASKLIST_ID and TASK_ID environment variables must be set")
        sys.exit(1)

    service = get_tasks_service()
    try:
        result = service.tasks().move(
            tasklist=tasklist_id,
            task=task_id,
            parent=parent if parent else None,
            previous=previous if previous else None
        ).execute()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    import asyncio
    
    commands = {
        'list_tasklists': list_tasklists,
        'create_tasklist': create_tasklist,
        'list_tasks': list_tasks,
        'create_task': create_task,
        'update_task': update_task,
        'move_task': move_task
    }

    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print(f"Usage: {sys.argv[0]} <command>")
        print(f"Available commands: {', '.join(commands.keys())}")
        sys.exit(1)

    asyncio.run(commands[sys.argv[1]]()) 