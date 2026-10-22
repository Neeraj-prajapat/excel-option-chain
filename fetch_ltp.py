import requests
import json
from api_credential import creds


# Fetch credentials
API_KEY = creds["API_KEY"]
AUTH_TOKEN = creds["AUTH_TOKEN"]


# Request data payload
data = {
    "mode": "FULL",
    "exchangeTokens": {
        "NSE": ["99926000"]
    }
}

# Request headers
headers = {
    'X-PrivateKey': API_KEY,
    'Accept': 'application/json, application/json',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.1.1',
    'X-ClientPublicIP': '203.0.113.1',
    'X-MACAddress': '00:1A:2B:3C:4D:5E',
    'X-UserType': 'USER',
    'Authorization': AUTH_TOKEN,
    'Content-Type': 'application/json'
}


# Function to fetch LTP
def fetch_ltp():
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

# Call the function
# send_request()

ltp =fetch_ltp()
print(ltp)











#?strike price data formate
 # {"status":true,"message":"SUCCESS","errorcode":"","data":{"fetched":[{"exchange":"NFO","tradingSymbol":"NIFTY16JAN2523100CE","symbolToken":"52533","ltp":115.8,"open":186,"high":218.5,"low":102,"close":176,"lastTradeQty":75,"exchFeedTime":"15-Jan-2025 14:02:58","exchTradeTime":"15-Jan-2025 14:02:58","netChange":-60.2,"percentChange":-34.2,"avgPrice":152.49,"tradeVolume":65655750,"opnInterest":3577800,"lowerCircuit":0.05,"upperCircuit":829.8,"totBuyQuan":779100,"totSellQuan":670800,"52WeekLow":0,"52WeekHigh":1581.65,"depth":{"buy":[{"price":115.85,"quantity":1350,"orders":3},{"price":115.8,"quantity":2175,"orders":13},{"price":115.75,"quantity":1875,"orders":12},{"price":115.7,"quantity":2850,"orders":12},{"price":115.65,"quantity":1725,"orders":11}],"sell":[{"price":116,"quantity":450,"orders":1},{"price":116.15,"quantity":1350,"orders":5},{"price":116.2,"quantity":2100,"orders":15},{"price":116.25,"quantity":1425,"orders":12},{"price":116.3,"quantity":2175,"orders":11}]}}],"unfetched":[]}}


#? nifty_data_formate
#{"status":true,"message":"SUCCESS","errorcode":"","data":{"fetched":[{"exchange":"NSE","tradingSymbol":"Nifty 50","symbolToken":"99926000","ltp":23180.35,"open":23250.45,"high":23293.65,"low":23146.45,"close":23176.05,"lastTradeQty":0,"exchFeedTime":"15-Jan-2025 14:27:49","exchTradeTime":"01-Jan-1970 05:30:00","netChange":4.3,"percentChange":0.02,"avgPrice":0,"tradeVolume":0,"opnInterest":0,"lowerCircuit":0,"upperCircuit":0,"totBuyQuan":0,"totSellQuan":0,"52WeekLow":0,"52WeekHigh":0,"depth":{"buy":[{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0}],"sell":[{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0},{"price":0,"quantity":0,"orders":0}]}}],"unfetched":[]}}  























# main.py
# from fetch_ltp import fetch_ltp

# def perform_analysis(ltp):
#     """Perform some analysis with the LTP."""
#     if ltp > 1000:
#         print(f"LTP of {ltp} is high, consider selling.")
#     else:
#         print(f"LTP of {ltp} is low, consider buying.")

# def main():
#     # Fetch the LTP
#     ltp = fetch_ltp()
#     if ltp is not None:
#         print(f"The Last Traded Price (LTP) is: {ltp}")
#         # Use LTP for analysis
#         perform_analysis(ltp)
#         # Use LTP for other tasks
#         print(f"LTP squared is: {ltp ** 2}")
#     else:
#         print("Failed to fetch LTP.")

# if __name__ == "__main__":
#     main()
