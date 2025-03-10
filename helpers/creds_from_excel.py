from SmartApi import SmartConnect
import xlwings as xw
import pyotp

def credential(excel_file_path: str) -> dict:
    """
    Reads credentials from the Excel sheet and initializes the SmartConnect API session.

    Parameters:
        excel_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet containing credentials.

    Returns:
        dict: A dictionary containing `api_key` and `auth_token`.
    """
    try:
        # Open the Excel workbook and access the specified sheet
        wb = xw.Book(excel_file_path)  # Use the provided path dynamically
        credential = wb.sheets["credential"]

        # Read credentials from the Excel sheet and ensure they are strings
        client_code = str(credential.range("b1").value).strip()
        password = str(int(credential.range("b2").value)).strip()  # Convert float to int, then to string
        api_key = str(credential.range("b3").value).strip()
        totp_secret = str(credential.range("b5").value).strip()
        correlation_id = str(credential.range("b6").value).strip()

        # Initialize API session
        obj = SmartConnect(api_key=api_key)
        data = obj.generateSession(client_code, password, pyotp.TOTP(totp_secret).now())
        auth_token = data['data']['jwtToken']
        feed_token = obj.getfeedToken()
        
        # Log feed token for debugging purposes
        # logger.info(f"Feed Token: {feed_token}")
        # print(auth_token)
        
        # Return the required values
        return {
            "API_KEY": api_key,
            "CLIENT_CODE": client_code,
            "AUTH_TOKEN": auth_token, 
            "FEED_TOKEN": feed_token,
            "CORRELATION_ID": correlation_id
        }

    except Exception as e:
        print(f"Error initializing API: {e}")
        return None
