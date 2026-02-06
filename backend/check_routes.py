import requests
import json

# Get the OpenAPI schema
response = requests.get("http://127.0.0.1:8000/openapi.json")
schema = response.json()

# Find paths containing "tasks"
print("Routes containing 'tasks':")
for path, methods in schema["paths"].items():
    if "tasks" in path.lower():
        print(f"  {path}: {list(methods.keys())}")
        
        # Show parameters for each method
        for method, details in methods.items():
            if 'parameters' in details:
                params = [p['name'] for p in details['parameters']]
                print(f"    {method.upper()} parameters: {params}")