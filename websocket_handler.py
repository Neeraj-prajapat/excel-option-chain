from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from datetime import datetime
from logzero import logger
import asyncio

class WebSocketHandler:
    def __init__(self, auth_token, api_key, client_code, correlation_id, feed_token, sheet, token_list):
        self.auth_token = auth_token
        self.api_key = api_key
        self.client_code = client_code
        self.feed_token = feed_token
        self.sheet = sheet
        self.token_list = token_list
        self.correlation_id = correlation_id  # You may want to pass this as a parameter
        self.mode = 3  # You may want to pass this as a parameter
        
        # Initialize the WebSocket
        self.sws = SmartWebSocketV2(self.auth_token, self.api_key, self.client_code, self.feed_token)
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close

    def on_data(self, wsapp, msg):
        try:
            token = int(msg.get("token"))  # Ensure token is treated as an integer
            ltp = msg.get("last_traded_price")/100
            oi = msg.get("open_interest")/75
            volume = msg.get("volume_trade_for_the_day")/75
            open_price = msg.get("open_price_of_the_day")/75
            high = msg.get("high_price_of_the_day")/100
            low = msg.get("low_price_of_the_day")/100
            close = msg.get("closed_price")/100
            ltp_chg = ltp - close
            
            timestamp = datetime.fromtimestamp(msg["exchange_timestamp"] / 1000).strftime('%Y-%m-%d %H:%M:%S')

            # Logging the received data
            logger.info(f"Received token: {token}, LTP: {ltp}, OI: {oi}, Timestamp: {timestamp}, VOLUME: {volume}")
            
            # Special token handling (NIFTY: 99926000)
            if token == 99926000:
                self.sheet['Q10'].value = ltp
                return   # Exit the function here, no further processing(for this function)
        
            # Iterate through the rows to find the matching token in F or R
            row = 12  # Start at the base row
            while self.sheet[f'F{row}'].value or self.sheet[f'AB{row}'].value:  # Stop when both are empty
                call_token = self.sheet[f'F{row}'].value
                put_token = self.sheet[f'AB{row}'].value

                if call_token == token:  # If the token matches the call token
                    self.sheet[f'P11'].value = "LTP"  
                    self.sheet[f'P{row}'].value = ltp  # Update LTP for the call
                    self.sheet[f'M11'].value = "OI"   
                    self.sheet[f'M{row}'].value = oi   # Update OI for the call
                    self.sheet[f'N11'].value = "VOLUME"
                    self.sheet[f'N{row}'].value = volume   # Update VOLUME for the call
                    self.sheet[f'C11'].value = "OPEN"
                    self.sheet[f'C{row}'].value = open_price  # Update OPEN for the call
                    self.sheet[f'D11'].value = "HIGH"
                    self.sheet[f'D{row}'].value = high   # Update HIGH for the call
                    self.sheet[f'E11'].value = "LOW"
                    self.sheet[f'E{row}'].value = low   # Update LOW for the call
                    self.sheet[f'B11'].value = "CLOSE"
                    self.sheet[f'B{row}'].value = close   # Update CLOSE for the call
                    self.sheet[f'O11'].value = "LTP CHG"
                    self.sheet[f'O{row}'].value = ltp_chg   # Update LTP CHANGE for the call
                    self.sheet[f'A11'].value = "TIMESTAMP"
                    self.sheet[f'A{row}'].value = timestamp  # Update timestamp for the call
                    break

                elif put_token == token:  # If the token matches the put token
                    self.sheet[f'R11'].value = "LTP"  
                    self.sheet[f'R{row}'].value = ltp  # Update LTP for the put
                    self.sheet[f'U11'].value = "OI"   
                    self.sheet[f'U{row}'].value = oi   # Update OI for the put
                    self.sheet[f'T11'].value = "VOLUME"
                    self.sheet[f'T{row}'].value = volume   # Update VOLUME for the put
                    self.sheet[f'AE11'].value = "OPEN"
                    self.sheet[f'AE{row}'].value = open_price  # Update OPEN for the put
                    self.sheet[f'AD11'].value = "HIGH"
                    self.sheet[f'AD{row}'].value = high   # Update HIGH for the put
                    self.sheet[f'AC11'].value = "LOW"
                    self.sheet[f'AC{row}'].value = low   # Update LOW for the put
                    self.sheet[f'AF11'].value = "CLOSE"
                    self.sheet[f'AF{row}'].value = close   # Update CLOSE for the put
                    self.sheet[f'S11'].value = "LTP CHG"
                    self.sheet[f'S{row}'].value = ltp_chg   # Update LTP CHANGE for the put
                    self.sheet[f'AG11'].value = "TIMESTAMP"
                    self.sheet[f'AG{row}'].value = timestamp  # Update timestamp for the put
                    break

                row += 1  # Move to the next row

        except Exception as e:
            logger.error(f"Error in on_data: {e}")

    def on_open(self, wsapp):
        logger.info("on open")
        self.sws.subscribe(self.correlation_id, self.mode, self.token_list)

    def on_error(self, wsapp, error):
        logger.error(error)

    def on_close(self, wsapp):
        logger.info("Close")

    async def start_websocket(self):
        try:
            logger.info("Starting WebSocket...")
            await self.sws.connect()
        except KeyboardInterrupt:
            logger.info("WebSocket connection terminated by user.")
        finally:
            logger.info("Closing WebSocket connection...")
            await self.sws.close_connection()

    def run(self):
        """Start the WebSocket connection"""
        asyncio.run(self.start_websocket())