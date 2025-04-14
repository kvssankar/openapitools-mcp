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
    print(json.dumps({"error": "API key is missing. Please provide 'x_api_key' in environment variables."}))
    sys.exit(1)

# Set up the API request
url = "https://stock.indianapi.in/news"
headers = {
    "X-Api-Key": api_key
}

try:
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Parse the JSON response
    news_data = response.json()
    
    # Output the result
    print(json.dumps(news_data, indent=2))
    
except requests.exceptions.RequestException as e:
    error_message = str(e)
    status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else 'unknown'
    print(json.dumps({
        "error": f"API request failed with status code {status_code}",
        "details": error_message
    }))
except Exception as e:
    print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}))
