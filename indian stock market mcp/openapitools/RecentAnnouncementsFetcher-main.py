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
stock_name = input_json.get('stockName')
api_key = env.get('x_api_key')

# API endpoint
url = 'https://stock.indianapi.in/recent_announcements'

# Parameters
params = {
    'stock_name': stock_name
}

# Headers
headers = {
    'X-Api-Key': api_key
}

try:
    # Make API request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse response
    result = response.json()
    
    # Format output
    output = json.dumps(result, indent=2)
    
    print(output)
except requests.exceptions.RequestException as e:
    error_message = f"Error fetching announcements: {str(e)}"
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_details = e.response.json()
            error_message += f" - {json.dumps(error_details)}"
        except:
            error_message += f" - Status code: {e.response.status_code}"
    
    print(json.dumps({"error": error_message}))