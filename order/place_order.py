import http.client
import json
from api_credential import creds


AUTH_TOKEN = creds["AUTH_TOKEN"]



# Create HTTPS connection
conn = http.client.HTTPSConnection("apiconnect.angelone.in")

# Payload for placing Nifty futures order (1 lot = 50 units)
payload = json.dumps({
    "variety": "NORMAL",
    "tradingsymbol": "NIFTY24NOVFUT",   # Example symbol, check latest expiry
    "symboltoken": "12345",             # Replace with actual token from instrument list
    "transactiontype": "BUY",
    "exchange": "NFO",
    "ordertype": "MARKET",
    "producttype": "INTRADAY",          # MIS for intraday, NRML for carry forward
    "duration": "DAY",
    "price": "0",                       # 0 for market order
    "quantity": 50                      # 1 lot of Nifty = 50
})

# Headers (replace placeholders with actual values)
headers = {
    'Authorization': AUTH_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-PrivateKey': 'API_KEY'
}

# Send request
conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload, headers)

# Get response
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
