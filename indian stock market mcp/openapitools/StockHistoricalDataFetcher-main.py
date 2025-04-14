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
period = input_json.get('period')
filter_type = input_json.get('filter')
api_key = env.get('x_api_key')

# Validate required parameters
if not stock_name or not period or not filter_type:
    print(json.dumps({
        'error': 'Missing required parameters. Please provide stockName, period, and filter.'
    }))
    sys.exit(1)

# API endpoint
url = 'https://stock.indianapi.in/historical_data'

# Parameters for the API request
params = {
    'stock_name': stock_name,
    'period': period,
    'filter': filter_type
}

# Headers
headers = {
    'X-Api-Key': api_key
}

try:
    # Make the API request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the response
    data = response.json()
    
    # Format and print the result
    result = {
        'stockName': stock_name,
        'period': period,
        'filter': filter_type,
        'data': data
    }
    
    print(json.dumps(result, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = f"Error fetching historical data: {str(e)}"
    if response and hasattr(response, 'text'):
        error_message += f"\nResponse: {response.text}"
    
    print(json.dumps({
        'error': error_message
    }))
    sys.exit(1)
except Exception as e:
    print(json.dumps({
        'error': f"Unexpected error: {str(e)}"
    }))
    sys.exit(1)
