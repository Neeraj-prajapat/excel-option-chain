import xlwings as xw
import logging
from datetime import datetime
from nifty_weekly_range import nifty_weekly_range
from get_workbook import wb


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def oi_change_extract():
    """Manages the 'nifty_snapshot_live' sheet in the workbook, backs up data, and recreates the table."""
    
    # Get the current time
    current_time = datetime.now().time()

    # Define the allowed time window (9:00 AM - 3:30 PM)
    start_time = datetime.strptime("08:55", "%H:%M").time()                                  #?Note:- Market ltp starts from 9:00 am and option chain at 9:15
    cutoff_time = datetime.strptime("15:30", "%H:%M").time()

    # Check if the current time is outside the 9:00 AM to 3:30 PM range
    if current_time < start_time or current_time > cutoff_time:
        logger.info("Running the process as it's outside the restricted time window.")
        
        ws_source = wb.sheets['nifty']

        # Turn off interaction and screen updates to improve performance
        wb.app.screen_updating = False
        wb.app.api.Interactive = False

        try:
            # Copy data from columns M (M12:M26) and U (U12:U26)
            call_OI_snap = ws_source.range('M12:M26').value
            put_OI_snap = ws_source.range('U12:U26').value
            
            # Convert data to 2D format (which xlwings expects for columns)
            # This forces each value into a list for column-based pasting.
            call_OI_snap = [[x] for x in call_OI_snap]  # Convert to 2D column format
            put_OI_snap = [[x] for x in put_OI_snap]  # Convert to 2D column format
            
            # Paste the data into columns AL (AL12:AL26) and AM (AM12:AM26)
            ws_source.range('AL12:AL26').value = call_OI_snap
            ws_source.range('AM12:AM26').value = put_OI_snap

            # Log success
            logger.info("Data successfully copied from M, U to AL, AM.")
            
            nifty_weekly_range(wb, current_time, start_time, cutoff_time)
            
            # Save the workbook after making changes
            wb.save()

        except Exception as e:
            logger.error(f"Error during snapshot append: {e}")
            print(f"Error during snapshot append: {e}")
        
        finally:
            # Re-enable interaction and screen updating
            wb.app.api.Interactive = True
            wb.app.screen_updating = True
        
    else:
        logger.info("Skipping 'nifty_snapshot_live' initialization as the current time is between 9:00 AM and 3:30 PM.")
        print("Skipping execution as it's between 9:00 AM and 3:30 PM.")


if __name__ == "__main__":
    # Open the workbook (replace with your actual file path)
    # wb_path = "option_chain.xlsm"  # Adjust the path to your Excel file
    try:
        # wb = xw.Book(wb_path)

        # Run the function
        oi_change_extract()
    
    except Exception as e:
        logger.error(f"Error opening the workbook: {e}")
        print(f"Error opening the workbook: {e}")
    
