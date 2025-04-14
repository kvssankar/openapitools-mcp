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

# API request
url = 'https://stock.indianapi.in/corporate_actions'
headers = {'X-Api-Key': api_key} if api_key else {}
params = {'stock_name': stock_name}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    result = json.dumps(data, indent=2)
except requests.exceptions.RequestException as e:
    result = f"Error fetching corporate actions data: {str(e)}"
except json.JSONDecodeError:
    result = f"Error parsing response: {response.text}"

# Output the result
print(result)