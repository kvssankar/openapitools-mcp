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
    print(json.dumps({"error": "X-Api-Key is required in environment variables"}))
    sys.exit(1)

# Make API request
url = "https://stock.indianapi.in/NSE_most_active"
headers = {"X-Api-Key": api_key}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as e:
    print(json.dumps({"error": f"API request failed: {str(e)}"})) 
except json.JSONDecodeError:
    print(json.dumps({"error": "Failed to parse API response as JSON", "response": response.text}))