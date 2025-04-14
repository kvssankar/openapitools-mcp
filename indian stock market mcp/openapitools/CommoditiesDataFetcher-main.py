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
    print(json.dumps({
        "error": "API key is missing. Please provide 'x_api_key' in the environment variables."
    }))
    sys.exit(1)

# Set up the request
url = "https://stock.indianapi.in/commodities"
headers = {
    "X-Api-Key": api_key
}

try:
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    commodities_data = response.json()
    
    # Print the formatted result
    print(json.dumps(commodities_data, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = str(e)
    status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else 'unknown'
    
    print(json.dumps({
        "error": f"Failed to fetch commodities data: {error_message}",
        "status_code": status_code
    }))
except Exception as e:
    print(json.dumps({
        "error": f"An unexpected error occurred: {str(e)}"
    }))