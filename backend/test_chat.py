import requests
import json
import time
from uuid import UUID

BASE_URL = "http://127.0.0.1:8000"

def test_chat_api():
    print("Testing Chat API functionality...")
    
    # Step 1: Sign up a new user
    signup_data = {
        "username": "chat_test_user_" + str(int(time.time())),
        "email": f"chat_test_{int(time.time())}@example.com",
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
    
    # Step 2: Test chat functionality
    print(f"\n2. Testing chat functionality for user {user_id}...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Send a message to the chat endpoint
    chat_data = {
        "message": "Hello, can you help me add a task?",
        "conversation_id": None  # Start a new conversation
    }
    
    # Note: According to the logs, the chat endpoint is at /api/{user_id}/chat
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    print(f"Chat response: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        chat_response = response.json()
        print(f"Conversation ID: {chat_response.get('conversation_id')}")
        print(f"AI Message: {chat_response.get('ai_message')}")
    else:
        print(f"Chat failed with status {response.status_code}")
    
    # Step 3: Try to add a task via chat
    print(f"\n3. Trying to add a task via chat...")
    task_data = {
        "message": "Please add a task: Buy groceries",
        "conversation_id": chat_response.get('conversation_id') if 'chat_response' in locals() and response.status_code == 200 else None
    }
    
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=task_data, headers=headers)
    print(f"Task addition via chat response: {response.status_code}")
    print(f"Response body: {response.text}")
    
    # Step 4: Check if the task was added
    print(f"\n4. Checking if the task was added...")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks", params={"page": 1, "page_size": 20}, headers=headers)
    print(f"Get tasks response: {response.status_code}")
    if response.status_code == 200:
        tasks_response = response.json()
        print(f"Number of tasks: {len(tasks_response.get('tasks', []))}")
        for task in tasks_response.get('tasks', []):
            print(f"  - Task: {task.get('title')} (ID: {task.get('id')})")
    else:
        print(f"Failed to get tasks: {response.text}")

if __name__ == "__main__":
    test_chat_api()