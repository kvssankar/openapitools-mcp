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
    print(json.dumps({"error": "API key is missing. Please provide x_api_key in environment variables."}))
    sys.exit(1)

# API endpoint
url = "https://stock.indianapi.in/price_shockers"

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
    data = response.json()
    
    # Print the formatted result
    print(json.dumps(data, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = str(e)
    if response and hasattr(response, 'text'):
        try:
            error_data = response.json()
            error_message = json.dumps(error_data)
        except:
            error_message = response.text
    
    print(json.dumps({"error": f"Failed to fetch price shockers data: {error_message}"}))
