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
measure_code = input_json.get('measureCode')
period_type = input_json.get('periodType')
data_type = input_json.get('dataType')
age = input_json.get('age')
x_api_key = env.get('x_api_key')

# API endpoint
url = 'https://stock.indianapi.in/stock_forecasts'

# Query parameters
params = {
    'stock_id': stock_id,
    'measure_code': measure_code,
    'period_type': period_type,
    'data_type': data_type,
    'age': age
}

# Headers
headers = {
    'X-Api-Key': x_api_key
}

try:
    # Make API request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse response
    result = response.json()
    
    # Format and print the result
    print(json.dumps(result, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = f"Error fetching stock forecasts: {str(e)}"
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_detail = e.response.json()
            error_message += f". Details: {json.dumps(error_detail)}"
        except:
            error_message += f". Status code: {e.response.status_code}"
    
    print(json.dumps({"error": error_message}))