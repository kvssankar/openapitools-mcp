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
api_key = env.get('xapikey')

# API call to get stock details
url = 'https://stock.indianapi.in/stock'
headers = {'X-Api-Key': api_key}
params = {'name': stock_name}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    stock_data = response.json()
    
    # Format the output
    result = json.dumps(stock_data, indent=2)
    print(result)
except requests.exceptions.RequestException as e:
    error_message = f"Error retrieving stock details: {str(e)}"
    if hasattr(e, 'response') and e.response is not None:
        error_message += f" - Status code: {e.response.status_code}"
        try:
            error_data = e.response.json()
            error_message += f" - Response: {json.dumps(error_data)}"
        except:
            error_message += f" - Response text: {e.response.text}"
    print(json.dumps({"error": error_message}))