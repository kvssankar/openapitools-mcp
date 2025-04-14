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

# Make API request to get BSE most active stocks
url = "https://stock.indianapi.in/BSE_most_active"
headers = {"X-Api-Key": api_key}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the response
    data = response.json()
    
    # Format and print the result
    print(json.dumps(data, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = str(e)
    if response and hasattr(response, 'text'):
        try:
            error_data = response.json()
            error_message = error_data.get('message', error_message)
        except:
            error_message = response.text or error_message
    
    print(json.dumps({"error": f"Failed to retrieve BSE most active stocks: {error_message}"}))
