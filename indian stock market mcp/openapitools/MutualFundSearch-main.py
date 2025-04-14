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
query = input_json.get('query')
api_key = env.get('x_api_key')

# API call
url = 'https://stock.indianapi.in/mutual_fund_search'
headers = {'X-Api-Key': api_key}
params = {'query': query}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    output = json.dumps(result, indent=2)
except requests.exceptions.RequestException as e:
    output = f"Error making API request: {str(e)}"
except json.JSONDecodeError:
    output = f"Error parsing API response: {response.text}"

# Print the output
print(output)