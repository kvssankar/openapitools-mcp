import json
import sys
import requests

# DONT CHANGE INPUT PART START
try:
    input_json = input_json
except:
    input_json = json.loads(sys.argv[1])
env = input_json.pop('openv', {})
# DONT CHANGE INPUT PART END

# Extract parameters and environment variables
query = input_json.get('query')
api_key = env.get('x_api_key')

# API endpoint
url = "https://stock.indianapi.in/industry_search"

# Prepare headers and parameters
headers = {}
if api_key:
    headers["X-Api-Key"] = api_key

params = {
    "query": query
}

try:
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the response
    result = response.json()
    
    # Format and print the result
    print(json.dumps(result, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = f"Error making API request: {str(e)}"
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_detail = e.response.json()
            error_message += f"\nAPI Error: {json.dumps(error_detail)}"
        except:
            error_message += f"\nStatus code: {e.response.status_code}"
    
    print(json.dumps({"error": error_message}))