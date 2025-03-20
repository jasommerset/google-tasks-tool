import os
import sys
from auth import client, get_tasks_service
from googleapiclient.errors import HttpError

def test_auth():
    """Test authentication and basic Tasks API functionality"""
    print("Testing Google Tasks Authentication...")
    
    # Test 1: Check if token exists
    token = os.getenv('GOOGLE_OAUTH_TOKEN')
    if not token:
        print("❌ GOOGLE_OAUTH_TOKEN not set")
        return False
    print("✓ GOOGLE_OAUTH_TOKEN found")
    
    try:
        # Test 2: Get service using generic client
        service = client()
        print("✓ Generic client creation successful")
        
        # Test 3: Get service using tasks-specific function
        tasks_service = get_tasks_service()
        print("✓ Tasks service creation successful")
        
        # Test 4: Try listing task lists (basic API call)
        result = tasks_service.tasklists().list().execute()
        print("✓ Successfully listed task lists")
        print(f"Found {len(result.get('items', []))} task lists")
        
        return True
        
    except ValueError as e:
        print(f"❌ Value Error: {e}")
        return False
    except HttpError as e:
        print(f"❌ HTTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_auth()
    sys.exit(0 if success else 1) 