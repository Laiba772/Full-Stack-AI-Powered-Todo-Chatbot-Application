import requests
import json
import time
from uuid import UUID

BASE_URL = "http://127.0.0.1:8000"

def test_full_chat_functionality():
    print("Testing Full Chat Functionality...")
    
    # Step 1: Sign up a new user
    signup_data = {
        "username": "test_user_" + str(int(time.time())),
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpassword123"
    }
    
    print("\n1. Signing up a new user...")
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"Signup response: {response.status_code}")
    
    if response.status_code != 201:
        print(f"Signup failed: {response.text}")
        return
    
    # Extract the access token and user ID
    response_data = response.json()
    access_token = response_data.get('access_token')
    user_id = response_data.get('user', {}).get('id')
    
    print(f"Access token: {access_token[:20]}..." if access_token else "No access token")
    print(f"User ID: {user_id}")
    
    if not access_token or not user_id:
        print("Failed to get access token or user ID")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test adding a task via chat
    print(f"\n2. Testing adding a task via chat for user {user_id}...")
    chat_data = {
        "message": "add a task: Complete project documentation"
    }
    
    # Use the correct path according to our routing: /api/{user_id}/chat
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    print(f"Chat add task response: {response.status_code}")
    if response.status_code == 200:
        chat_response = response.json()
        print(f"Chat response: {chat_response.get('response', 'No response field')}")
    else:
        print(f"Chat failed: {response.text}")
    
    # Step 3: Test showing tasks via chat
    print(f"\n3. Testing showing tasks via chat...")
    chat_data = {
        "message": "show my tasks"
    }
    
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    print(f"Chat show tasks response: {response.status_code}")
    if response.status_code == 200:
        chat_response = response.json()
        print(f"Chat response: {chat_response.get('response', 'No response field')}")
    else:
        print(f"Chat failed: {response.text}")
    
    # Step 4: Verify tasks exist using the tasks API directly
    print(f"\n4. Verifying tasks using tasks API...")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks", params={"page": 1, "page_size": 20}, headers=headers)
    print(f"Get tasks response: {response.status_code}")
    if response.status_code == 200:
        tasks_response = response.json()
        print(f"Number of tasks: {len(tasks_response.get('tasks', []))}")
        for task in tasks_response.get('tasks', []):
            print(f"  - Task: {task.get('title')} (ID: {task.get('id')}, Completed: {task.get('is_complete')})")
    else:
        print(f"Failed to get tasks: {response.text}")

if __name__ == "__main__":
    test_full_chat_functionality()