import requests
import json
from uuid import UUID
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api_flow():
    print("Testing API flow...")
    
    # Step 1: Sign up a new user
    signup_data = {
        "username": "testuser_" + str(int(time.time())),
        "email": f"testuser_{int(time.time())}@example.com",
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
    
    # Step 2: Try to get tasks for this user
    print(f"\n2. Getting tasks for user {user_id}...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Using the path that matches the frontend expectation: /api/users/{user_id}/tasks
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks", params={"page": 1, "page_size": 20}, headers=headers)
    print(f"Get tasks response: {response.status_code}")
    print(f"Response body: {response.text}")

    # Step 3: Add a task for this user
    print(f"\n3. Adding a task for user {user_id}...")
    task_data = {
        "title": "Test task",
        "description": "This is a test task"
    }

    # Using the path that matches the frontend expectation
    response = requests.post(f"{BASE_URL}/api/users/{user_id}/tasks", json=task_data, headers=headers)
    print(f"Add task response: {response.status_code}")
    print(f"Response body: {response.text}")

    # Step 4: Get tasks again to see if the new task appears
    print(f"\n4. Getting tasks again for user {user_id}...")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}/tasks", params={"page": 1, "page_size": 20}, headers=headers)
    print(f"Get tasks response: {response.status_code}")
    print(f"Response body: {response.text}")

if __name__ == "__main__":
    test_api_flow()