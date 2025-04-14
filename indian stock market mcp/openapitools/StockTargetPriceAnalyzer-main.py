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
stock_id = input_json.get('stockId')
api_key = env.get('x_api_key')

# API endpoint
url = "https://stock.indianapi.in/stock_target_price"

# Parameters
params = {
    "stock_id": stock_id
}

# Headers
headers = {
    "X-Api-Key": api_key
}

try:
    # Make API request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse response
    result = response.json()
    
    # Format output
    output = {
        "success": True,
        "data": result
    }
    
except requests.exceptions.RequestException as e:
    # Handle API request errors
    output = {
        "success": False,
        "error": str(e)
    }
except Exception as e:
    # Handle other errors
    output = {
        "success": False,
        "error": f"An unexpected error occurred: {str(e)}"
    }

# Print output as JSON string
print(json.dumps(output))