import xlwings as xw
import logging
from datetime import datetime, timedelta
import math

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def nifty_weekly_range(wb, current_time, start_time, cutoff_time):
    """Manages the 'nifty_snapshot_live' sheet in the workbook, backs up data, and recreates the table."""
    
    # Get the current date and time
    # current_time = datetime.now().time()
    current_date = datetime.now().date()
    
    ws_source = wb.sheets['nifty']
    
    # Define the allowed time window (9:00 AM - 3:30 PM)
    # start_time = datetime.strptime("08:55", "%H:%M").time()
    # cutoff_time = datetime.strptime("15:30", "%H:%M").time()

    # Extract and format the expiry date (assuming it's in cell B1)
    nifty_expiry_date = ws_source.range('B1').value

    if isinstance(nifty_expiry_date, datetime):
        nifty_expiry_date = nifty_expiry_date.date()  # Ensure it's a date type
    else:
        logger.error("Invalid expiry date format in B1")
        return

    # Calculate the matched date (6 days before expiry)
    matched_date = nifty_expiry_date - timedelta(days=6)
    prev_matched_date = nifty_expiry_date - timedelta(days=7)

    # Check if the current time is outside the 9:00 AM to 3:30 PM range and the date matches
    # if (current_time < start_time or current_time > cutoff_time) and current_date == matched_date:
    if (current_time < start_time and current_date == matched_date) or (current_time > cutoff_time and current_date == prev_matched_date):
              
        # if current_time < start_time and current_date == matched_date:
        logger.info("Calculating Nifty Weekly Range...")
        
        # Turn off interaction and screen updates to improve performance
        # wb.app.screen_updating = False
        # wb.app.api.Interactive = False

        try:
            put_otm = ws_source.range('R19').value
            call_otm = ws_source.range('P20').value
            nifty_ltp_closed = ws_source.range('Q10').value

            if None in (put_otm, call_otm, nifty_ltp_closed):
                raise ValueError("One or more required values are missing in the sheet.")

            total_otm_premium = call_otm + put_otm
            # nifty_weekly_support = round(nifty_ltp_closed -  total_otm_premium, 2)      # Rounded to 2 decimals
            # nifty_weekly_resistance = round(nifty_ltp_closed +  total_otm_premium, 2)
            
            nifty_weekly_support =  math.ceil(nifty_ltp_closed -  total_otm_premium)   # Always round up
            nifty_weekly_resistance = math.ceil(nifty_ltp_closed +  total_otm_premium)

            # Paste the calculated data
            ws_source.range('C4').value = nifty_weekly_support
            ws_source.range('C5').value = nifty_weekly_resistance

            logger.info(f"Updated weekly range: Support={nifty_weekly_support}, Resistance={nifty_weekly_resistance}")
        
        except Exception as e:
            logger.error(f"Error during data processing: {e}")
        
        # finally:
        #     # Re-enable interaction and screen updating
        #     wb.app.api.Interactive = True
        #     wb.app.screen_updating = True

    else:
        logger.info("Skipping execution as it's between 9:00 AM and 3:30 PM or the date doesn't match.")

# if __name__ == "__main__":
#     # Open the workbook (replace with your actual file path)
#     wb_path = "option_chain.xlsm"  # Adjust the path to your Excel file
#     try:
#         wb = xw.Book(wb_path)
#         nifty_weekly_range(wb)
#     except Exception as e:
#         logger.error(f"Error opening the workbook: {e}")
