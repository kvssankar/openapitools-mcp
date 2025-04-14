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

# Extract API key from environment variables
api_key = env.get('x_api_key')

if not api_key:
    print(json.dumps({"error": "API key is missing. Please provide 'x_api_key' in environment variables."}))
    sys.exit(1)

# API endpoint
url = "https://stock.indianapi.in/trending"

# Headers with API key
headers = {
    "X-Api-Key": api_key
}

try:
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    trending_stocks = response.json()
    
    # Print the formatted result
    print(json.dumps(trending_stocks, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = f"Error fetching trending stocks: {str(e)}"
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_detail = e.response.json()
            error_message += f". Details: {json.dumps(error_detail)}"
        except:
            error_message += f". Status code: {e.response.status_code}"
    
    print(json.dumps({"error": error_message}))
