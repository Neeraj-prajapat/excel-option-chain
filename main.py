import threading
import time
import pythoncom
from api_credential import creds
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from get_filtered_tokens import get_filtered_tokens
from datetime import datetime
from logzero import logger
from snapshot_oi import append_snapshot_to_table
from nifty_snapshot_table import manage_nifty_snapshot_table
from oi_change_extract import  oi_change_extract
from get_workbook import wb

# Fetch credentials
API_KEY = creds["API_KEY"]
CLIENT_CODE = creds["CLIENT_CODE"]
FEED_TOKEN = creds["FEED_TOKEN"]
AUTH_TOKEN = creds["AUTH_TOKEN"]
CORRELATION_ID = creds["CORRELATION_ID"]


# WebSocket setup
token_value = get_filtered_tokens()
token_list = [
    {"exchangeType": 2, "tokens": token_value},
    {"exchangeType": 1, "tokens": ["99926000"]}
]

# Global variables
latest_data = {}  # Dictionary to store the latest data for each token
sws = None
sheet = None

 
def initialize_excel():
    global sheet
    sheet_name = "nifty"

    if sheet_name in [s.name for s in wb.sheets]:
        sheet = wb.sheets[sheet_name]
    else:
        sheet = wb.sheets.add(sheet_name)

    # Initialize token layout
    base_row = 12
    tokens = sorted(map(int, token_value))
    for i in range(0, len(tokens), 2):
        call_token = tokens[i]
        put_token = tokens[i + 1] if i + 1 < len(tokens) else None
        sheet[f'F{base_row}'].value = call_token
        if put_token:
            sheet[f'AB{base_row}'].value = put_token
        base_row += 1
        
    # Define column headers ✅ (Loop + Dictionary) is better in terms of performance and efficiency, especially when dealing with larger data.
    headers = {
        'B3': '=MROUND(Q10, 50)', 'P11': "LTP", 'M11': "OI", 'N11': "VOLUME",
        'C11': "OPEN", 'D11': "HIGH", 'E11': "LOW", 'B11': "CLOSE", 'O11': "LTP CHG",
        'A11': "TIMESTAMP", 'R11': "LTP", 'U11': "OI", 'T11': "VOLUME",
        'AE11': "OPEN", 'AD11': "HIGH", 'AC11': "LOW", 'AF11': "CLOSE",
        'S11': "LTP CHG", 'AG11': "TIMESTAMP"
    }

    for cell, value in headers.items():
        sheet[cell].value = value
        
    manage_nifty_snapshot_table(wb)
    oi_change_extract()
        

def on_data(wsapp, msg):
    try:
        token = int(msg.get("token"))
        data = {
            "token": token,
            "ltp": msg.get("last_traded_price") / 100,
            "oi": msg.get("open_interest") / 75,
            "volume": msg.get("volume_trade_for_the_day") / 75,
            "open": msg.get("open_price_of_the_day") / 75,
            "high": msg.get("high_price_of_the_day") / 100,
            "low": msg.get("low_price_of_the_day") / 100,
            "close": msg.get("closed_price") / 100,
            "timestamp": datetime.fromtimestamp(msg["exchange_timestamp"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        }
        # Update the dictionary with the latest data for this token
        latest_data[token] = data
        logger.debug(f"Updated data for token: {token}")
        logger.info(f"Received token: {token}, LTP: {data['ltp']}, OI: {data['oi']}, Timestamp: {data['timestamp']}, VOLUME: {data['volume']}")
    except Exception as e:
        logger.error(f"Data processing error: {e}")

def process_excel_updates():
    pythoncom.CoInitialize()
    last_snapshot_time = time.time()  # Track last snapshot time

    try:
        while True:
            # Update Excel with latest WebSocket data
            for token, data in latest_data.copy().items():
                update_excel(data)

            # Append snapshot every 60 seconds
            if time.time() - last_snapshot_time >= 60:
                append_snapshot_to_table(wb)
                logger.info("Snapshot appended successfully.")
                last_snapshot_time = time.time()  # Reset snapshot timer

            time.sleep(0.5)  # Adjust the sleep interval as necessary
    except KeyboardInterrupt:
        pass
    finally:
        pythoncom.CoUninitialize()

def update_excel(data):
    try:
        token = data["token"]
        
        if token == 99926000:
            sheet['Q10'].value = data["ltp"]  # Update Q10 for token 99926000
        
        row = 12
        while sheet[f'F{row}'].value or sheet[f'AB{row}'].value:
            call_token = sheet[f'F{row}'].value
            put_token = sheet[f'AB{row}'].value

            if call_token == token:
                update_call_row(row, data)
                break
            elif put_token == token:
                update_put_row(row, data)
                break
            row += 1
    except Exception as e:
        logger.error(f"Excel update failed: {e}")

def update_call_row(row, data):
    sheet[f'P{row}'].value = data["ltp"]
    sheet[f'M{row}'].value = data["oi"]
    sheet[f'N{row}'].value = data["volume"]
    sheet[f'C{row}'].value = data["open"]
    sheet[f'D{row}'].value = data["high"]
    sheet[f'E{row}'].value = data["low"]
    sheet[f'B{row}'].value = data["close"]
    sheet[f'O{row}'].value = data["ltp"] - data["close"]
    sheet[f'A{row}'].value = data["timestamp"]

def update_put_row(row, data):
    sheet[f'R{row}'].value = data["ltp"]
    sheet[f'U{row}'].value = data["oi"]
    sheet[f'T{row}'].value = data["volume"]
    sheet[f'AE{row}'].value = data["open"]
    sheet[f'AD{row}'].value = data["high"]
    sheet[f'AC{row}'].value = data["low"]
    sheet[f'AF{row}'].value = data["close"]
    sheet[f'S{row}'].value = data["ltp"] - data["close"]
    sheet[f'AG{row}'].value = data["timestamp"]

def websocket_thread():
    sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)
    
    def on_open(wsapp):
        logger.info("WebSocket connected")
        sws.subscribe(CORRELATION_ID, 3, token_list)

    def on_error(wsapp, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(wsapp):
        logger.info("WebSocket closed")

    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    try:
        logger.info("Starting WebSocket...")
        sws.connect()
    except Exception as e:
        logger.error(f"WebSocket connection failed: {e}")
    finally:
        sws.close_connection()

def main():
    global latest_data
    latest_data = {}  # Reset the dictionary at the start of each run
    try:
        initialize_excel()
        logger.info("Excel initialized")
        
        # Start WebSocket thread
        ws_thread = threading.Thread(target=websocket_thread, daemon=True)
        ws_thread.start()
        
        # Process Excel updates in the main thread (including snapshot every 60 seconds)
        process_excel_updates()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    finally:
        logger.info("Saving and closing workbook...")
        # wb.save()
        # wb.close()
        logger.info("Cleanup complete")

if __name__ == "__main__":
    main()



