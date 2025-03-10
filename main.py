# Import credentials from config.py
from helpers.creds_from_excel import credential
from helpers.get_filtered_tokens import get_filtered_tokens
from helpers.fetch_ltp import fetch_ltp
from websocket_handler import WebSocketHandler  # Import the new WebSocket handler
import xlwings as xw
from datetime import datetime
from logzero import logger

# Fetch credentials
excel_file_path = "option_chain.xlsm"
credentials = credential(excel_file_path)
API_KEY = credentials["API_KEY"]
CLIENT_CODE = credentials["CLIENT_CODE"]
FEED_TOKEN = credentials["FEED_TOKEN"]
AUTH_TOKEN = credentials["AUTH_TOKEN"]
CORRELATION_ID = credentials["CORRELATION_ID"]

# Fetch LTP
strike_price_roundup_ltp = fetch_ltp(API_KEY, AUTH_TOKEN)

# WebSocket setup
token_value = get_filtered_tokens(excel_file_path)
token_list = [
    {
        "exchangeType": 2,
        "tokens": token_value
    },
    {
        "exchangeType": 1,
        "tokens": ["99926000"]
    }
]

# Excel setup
excel_file_path ="option_chain.xlsm"
wb = xw.Book(excel_file_path)
sheet_name = "nifty"
if sheet_name not in [s.name for s in wb.sheets]:
    sheet = wb.sheets.add(sheet_name)
else:
    sheet = wb.sheets[sheet_name]

# Rearrange tokens and set up initial rows
base_row = 12
tokens = sorted(map(int, token_value))
for i in range(0, len(tokens), 2):
    call_token = tokens[i]
    put_token = tokens[i + 1] if i + 1 < len(tokens) else None
    sheet[f'F{base_row}'].value = call_token
    if put_token:
        sheet[f'AB{base_row}'].value = put_token
    base_row += 1

# Function to mimic Excel's MROUND
def mround(number, multiple):
    return round(number / multiple) * multiple

number = strike_price_roundup_ltp # Original number
multiple = 50 # Adjust the step to 50000 for desired output

# Apply mround function to get nearest multiple
nifty_strike_price = mround(number, multiple)
print(nifty_strike_price)

# Assign the same value to two cells
sheet["Q32"].value = nifty_strike_price
sheet["P8"].value = strike_price_roundup_ltp

# Initialize and run the WebSocket handler
ws_handler = WebSocketHandler(
    auth_token=AUTH_TOKEN,
    api_key=API_KEY,
    client_code=CLIENT_CODE,
    correlation_id=CORRELATION_ID,
    feed_token=FEED_TOKEN,
    sheet=sheet,
    token_list=token_list
)

# Start the WebSocket connection
ws_handler.run()
