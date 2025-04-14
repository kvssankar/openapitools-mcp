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
    print(json.dumps({"error": "API key not provided. Please set x_api_key in environment variables."}))
    sys.exit(1)

# API endpoint
url = "https://stock.indianapi.in/ipo"

# Headers with API key
headers = {
    "X-Api-Key": api_key
}

try:
    # Make API request
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse and return the response
    ipo_data = response.json()
    print(json.dumps(ipo_data, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = str(e)
    try:
        # Try to get more detailed error message from response
        error_data = response.json() if 'response' in locals() else {}
        error_message = f"{error_message}: {json.dumps(error_data)}"
    except:
        pass
    
    print(json.dumps({"error": error_message}))
