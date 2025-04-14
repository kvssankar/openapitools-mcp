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

# API call to get mutual fund details
url = 'https://stock.indianapi.in/mutual_funds_details'
headers = {'X-Api-Key': api_key}
params = {'stock_name': stock_name}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    # Process the response
    result = response.json()
    
    # Format the output
    formatted_result = json.dumps(result, indent=2)
    print(formatted_result)
    
except requests.exceptions.RequestException as e:
    error_message = f"Error retrieving mutual fund details: {str(e)}"
    print(json.dumps({"error": error_message}))
except Exception as e:
    error_message = f"Unexpected error: {str(e)}"
    print(json.dumps({"error": error_message}))
