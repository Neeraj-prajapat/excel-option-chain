import requests
import json

# Function to fetch LTP
def fetch_ltp(api_key=None, auth_token=None):
    # If API_KEY and AUTH_TOKEN are not provided as arguments, try to get them from credential
    if api_key is None or auth_token is None:
        from .creds_from_excel import credential
        credentials = credential("option_chain.xlsm")
        api_key = credentials["API_KEY"]
        auth_token = credentials["AUTH_TOKEN"]
    
    # Request data payload
    data = {
        "mode": "FULL",
        "exchangeTokens": {
            "NSE": ["99926000"]
        }
    }

    # Request headers
    headers = {
        'X-PrivateKey': api_key,
        'Accept': 'application/json, application/json',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': '192.168.1.1',
        'X-ClientPublicIP': '203.0.113.1',
        'X-MACAddress': '00:1A:2B:3C:4D:5E',
        'X-UserType': 'USER',
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }

    url = 'https://apiconnect.angelone.in/rest/secure/angelbroking/market/v1/quote/'
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            ltp = response_data['data']['fetched'][0]['ltp']
            return ltp
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None