import pandas as pd
import requests
from datetime import date

def get_filtered_tokens(excel_file_path=None):
    
    from .fetch_ltp import fetch_ltp
    
    # If excel_file_path is provided, pass it to fetch_ltp
    if excel_file_path:
        from .creds_from_excel import credential
        credentials = credential(excel_file_path)
        api_key = credentials["API_KEY"]
        auth_token = credentials["AUTH_TOKEN"]
        ltp = fetch_ltp(api_key, auth_token)
    else:
        ltp = fetch_ltp()
        
    if ltp is None:
        raise ValueError("Failed to fetch LTP.")

    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    d = requests.get(url).json() 
    token_df = pd.DataFrame.from_dict(d)
    token_df["expiry"] = pd.to_datetime(token_df["expiry"] , format = "mixed").apply(lambda x: x.date()) 
    token_df = token_df.astype({"strike": float})

    # Filter for NIFTY and OPTIDX
    nifty_optidx_df = token_df[
        (token_df.name == "NIFTY") &
        (token_df.instrumenttype == "OPTIDX")
    ]

    nifty_optidx_expiry = nifty_optidx_df.expiry.unique()
    # print(nifty_optidx_expiry)


    # Function to mimic Excel's MROUND
    def mround(number, multiple):
        return round(number / multiple) * multiple

    # Example
    number = ltp *100 # Original number
    multiple = 5000  # Adjust the step to 50000 for desired output

    # Apply mround function to get nearest multiple
    nifty_ltp = mround(number, multiple)

    # Generate 20 numbers above and 20 numbers below with a step of 50000
    strike_prices = [nifty_ltp + i * multiple for i in range(-20, 21)]

    # Print the result
    # print(strike_prices)


    # Assuming nifty_optidx_df is your DataFrame and 'strike' and 'expiry' are columns

    # filtered_tokens = nifty_optidx_df[
    #     nifty_optidx_df['strike'].isin(strike_prices) & 
    #     nifty_optidx_df['expiry'].isin([date(2025, 1, 16)])
    # ]

    # Filter tokens based on strike and expiry
    expiry_date = date(2025, 1, 30)
    filtered_tokens = nifty_optidx_df[
        nifty_optidx_df['strike'].isin(strike_prices) & 
        nifty_optidx_df['expiry'].isin([expiry_date])
    ]
        
    # Return the resulting tokens
    return filtered_tokens['token'].tolist()





