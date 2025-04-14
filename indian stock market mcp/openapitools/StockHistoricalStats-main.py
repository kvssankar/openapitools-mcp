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
stats = input_json.get('stats')
api_key = env.get('x_api_key')

# API endpoint
url = 'https://stock.indianapi.in/historical_stats'

# Parameters for the request
params = {
    'stock_name': stock_name,
    'stats': stats
}

# Headers with API key
headers = {
    'X-Api-Key': api_key
}

try:
    # Make the API request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    # Format the result
    result = {
        'status': 'success',
        'data': data
    }
    
except requests.exceptions.RequestException as e:
    # Handle request errors
    result = {
        'status': 'error',
        'message': str(e)
    }
    if hasattr(e, 'response') and e.response is not None:
        try:
            result['details'] = e.response.json()
        except:
            result['details'] = e.response.text

# Output the result as a JSON string
print(json.dumps(result, indent=2))