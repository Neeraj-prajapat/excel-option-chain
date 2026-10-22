import pandas as pd
import requests
from datetime import date
from fetch_ltp import ltp
from get_workbook import wb

def get_filtered_tokens():
        
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

   # Extract unique expiries, sort them
    nifty_optidx_expiry = sorted(nifty_optidx_df.expiry.unique())
    # print("Available Expiries:", nifty_optidx_expiry)


    # Function to mimic Excel's MROUND
    def mround(number, multiple):
        return round(number / multiple) * multiple

    # Example
    number = ltp *100 # Original number
    multiple = 5000  # Adjust the step to 50000 for desired output

    # Apply mround function to get nearest multiple
    nifty_ltp = mround(number, multiple)
    # print("Nifty Roundup LTP to extract Strike Prices:", nifty_ltp)

    #? Open Excel
    # excel_file_path = "option_chain.xlsm"
    # wb = xw.Book(excel_file_path)
    sheet_name = "nifty"
    sheet = wb.sheets[sheet_name]
    
    #? Generating Strike prices
    # # Add dropdown in B2 for No_of_strike_price
    # options = [7, 8, 10, 11, 12, 15]
    # sheet.range("AK1").value = [[opt] for opt in options]  # Write options vertically in AK1 down
    # dropdown_range = f'$AK$1:$AK${len(options)}'
    # sheet.range("B2").api.Validation.Delete()
    # sheet.range("B2").api.Validation.Add(
    #     Type=3, AlertStyle=1, Formula1=f'={dropdown_range}'
    # )
    
    # Read the value for No_of_strike_price from the Excel cell (for example, cell A1)
    try:
        val = sheet.range('B2').value
        if val is None:
            No_of_strike_price = 7  # Default value if cell is empty
        else:
            No_of_strike_price = int(val)  # Convert to int if value exists
    except Exception as e:
        print("Error reading B2:", e)
        No_of_strike_price = 7  # Fallback default if something unexpected happens
        
    print("Number of Strike Prices (from Excel):", No_of_strike_price)
        
    # Generate 20 numbers above and 20 numbers below with a step of 50000
    # strike_prices = [nifty_ltp + i * multiple for i in range(-20, 21)]
    # strike_prices = [nifty_ltp + i * multiple for i in range(-7, 8)]
    strike_prices = [nifty_ltp + i * multiple for i in range(-No_of_strike_price, No_of_strike_price + 1)]
    print("Generated Strike Prices:", strike_prices)
    #?end

    
    # Write expiries to Q2 onwards
    expiry_column = [[exp.strftime('%Y-%m-%d')] for exp in nifty_optidx_expiry]
    sheet.range("AJ1").value = expiry_column
    
    # # Hide column Z (optional)
    # sheet.range("Z1").expand('down').columns.api.EntireColumn.Hidden = True
    
    
    # Set data validation (dropdown) in Q1 using Excel formula
    # last_row = len(nifty_optidx_expiry)  # Q2 to Q(last_row)
    # dv_range = f"$AJ$1:$AJ${last_row}"
    # formula = f"='{sheet_name}'!{dv_range}"                                       #? Use single quotes in sheet reference in case of special chars
    # # formula = f"='nifty'!{dv_range}"
    # sheet.range("B1").api.Validation.Delete()  # Clear old validation if any
    # sheet.range("B1").api.Validation.Add(
    #     Type=3,  # Type 3 = List validation (dropdown)
    #     AlertStyle=1,
    #     Operator=1,          # Required by COM (ignored for Type=3)
    #     Formula1=formula,
    #     Formula2=""         # Must supply 5th arg
    # )

    # Read selected expiry from Q1
    selected_expiry_str = sheet.range("B1").value
    print("Selected Expiry from Excel:", selected_expiry_str)

    # If expiry not selected, take latest expiry (nearest date)
    if selected_expiry_str:
        try:
            selected_expiry = pd.to_datetime(selected_expiry_str).date()
        except:
            print("Invalid expiry format in Excel. Using latest expiry.")
            selected_expiry = nifty_optidx_expiry[0]
    else:
        selected_expiry = nifty_optidx_expiry[0]
        print("No expiry selected. Using latest expiry:", selected_expiry)
        
     # Check if the selected expiry is in the past
    today = date.today()
    if selected_expiry < today:
        print(f"Selected expiry {selected_expiry} is expired (today is {today}).")
        # Find the next valid expiry (first expiry that is >= today)
        future_expiries = [exp for exp in nifty_optidx_expiry if exp >= today]
        if future_expiries:
            selected_expiry = future_expiries[0]
            print(f"Auto-updating expiry to the next available expiry: {selected_expiry}")
        else:
            raise ValueError("No valid future expiries available.")

    # Filter tokens using selected expiry
    filtered_tokens = nifty_optidx_df[
        nifty_optidx_df['strike'].isin(strike_prices) &
        nifty_optidx_df['expiry'].isin([selected_expiry])
    ]

    # Write strike prices to Q12 downwards
    strike_prices_column = [[price/100] for price in strike_prices]
    sheet.range("Q12").value = strike_prices_column
    
    
    
    
    
    
    # Assuming nifty_optidx_df is your DataFrame and 'strike' and 'expiry' are columns
    # Filter tokens based on strike and expiry
    # expiry_date = date(2025, 3, 20)
    # filtered_tokens = nifty_optidx_df[
    #     nifty_optidx_df['strike'].isin(strike_prices) & 
    #     nifty_optidx_df['expiry'].isin([expiry_date])
    # ]
        

    return filtered_tokens['token'].tolist()





