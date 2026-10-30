import xlwings as xw
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define the range labels as separate variables
var_75 = "75% to <80%"
var_80 = "80% to <85%"
var_85 = "85% to <90%"
var_90 = "90% to <95%"
var_95 = "95% to <100%"
var_100 = "=100%"
var_other = "Other"

# Define a helper function that returns the appropriate label based on the ratio
def categorize_ratio(ratio):
    if 0.75 <= ratio < 0.8:
        return var_75
    elif 0.8 <= ratio < 0.85:
        return var_80
    elif 0.85 <= ratio < 0.9:
        return var_85
    elif 0.9 <= ratio < 0.95:
        return var_90
    elif 0.95 <= ratio < 1:
        return var_95
    elif ratio == 1:
        return var_100
    else:
        return var_other

# Function to check conditions and execute a sell put trade
# def sell_put_trade(resistance_status, support_status, market_ltp, weekly_bottom, threshold=0.02):
def sell_put_trade(resistance_status, support_status, market_ltp, weekly_bottom, max_diff=40):
    """
    Executes a sell put trade if:
      - resistance_status is "wtt_resistance"
      - support_status is "wtt_support"
      - market_ltp is within 'threshold' percent of the weekly bottom
    """
    if resistance_status == "wtt_resistance" and (support_status == "wtt_support" or support_status == "str_support"):
        # if abs(market_ltp - weekly_bottom) / weekly_bottom <= threshold:
        if abs(market_ltp - weekly_bottom)  <= max_diff:
            print("Trade Conditions Met:")
            # Insert your trade API call here to execute a sell put trade
            print("Executing SELL PUT trade...")
            return True
        # else:
        #     print("Market LTP is not near the weekly bottom.")
    # else:
    #     print("Trade conditions not met: Resistance is not wtt or support is not strong.")
    return False

def algo(wb):
    current_time = datetime.now().time()
    start_time = datetime.strptime("09:15", "%H:%M").time()
    cutoff_time = datetime.strptime("15:30", "%H:%M").time()
    
    if current_time > start_time and current_time < cutoff_time:
        ws_source = wb.sheets['nifty']
        try:
            # Fetch data from Excel columns M (M12:M26) and U (U12:U26)
            call_oi = ws_source.range('M12:M26').value
            put_oi = ws_source.range('U12:U26').value
            weekly_range_support = ws_source.range('C5')
            weekly_range_resistance = ws_source.range('C4')
            market_ltp = ws_source.range('Q10')

            # Compute the maximum open interest from call data (assuming this is what you need)
            max_call_oi = max(call_oi)          # 100%
            max_put_oi = max(put_oi)            # 100%
            
            resistance = max_call_oi
            support = max_put_oi
            
            # Initialize resistance and support positions
            max_index_call = call_oi.index(max_call_oi)  # Resistance position (max call OI)
            max_index_put = put_oi.index(max_put_oi)  # Support position (max put OI)
                     
            # call_categories = []
            # for oi in call_oi:
            #     ratio = oi / max_call_oi
            #     category = categorize_ratio(ratio)
            #     call_categories.append(category)
                
            
            # Find second-highest for calls and puts, if they exist
            sorted_call_oi = sorted(call_oi, reverse=True)
            sorted_put_oi  = sorted(put_oi, reverse=True)

            # second_highest_call = sorted_call_oi[1] if len(sorted_call_oi) > 1 else None
            # second_highest_put  = sorted_put_oi[1] if len(sorted_put_oi) > 1 else None
            
            second_highest_call = sorted_call_oi[1] 
            second_highest_put  = sorted_put_oi[1] 
            
            second_index = put_oi.index(second_highest_put)
            second_index = call_oi.index(second_highest_put)
            
            # Determine the category of the second-highest call OI
            second_call_category = None
            ratio_call = second_highest_call / max_call_oi
            cat_call = categorize_ratio(ratio_call)
            if cat_call in [var_75, var_80, var_85, var_90, var_95]:
                second_call_category = cat_call

            # Determine the category of the second-highest put OI
            second_put_category = None
            ratio_put = second_highest_put / max_put_oi
            cat_put = categorize_ratio(ratio_put)
            if cat_put in [var_75, var_80, var_85, var_90, var_95]:
                second_put_category = cat_put

            
            
            
            resistance_status = "str_resistance"
             # For calls, check if a valid second call exists and then determine resistance status
            if second_call_category is not None:
                # Find the indices in the original call_oi list
                max_index = call_oi.index(max_call_oi)
                second_index = call_oi.index(second_highest_call)
                # If the second-highest appears below the max cell (i.e. higher index), assign "wtt_resistance"
                # If it appears above the max cell (i.e. lower index), assign "wtb_resistance"
                if second_index > max_index:
                    resistance_status = "wtt_resistance"
                else:
                    resistance_status = "wtb_resistance"
            # else:
            #     # If no valid second call exists, then use the max call OI as resistance.
            #     # str_resistance = f"Max call OI resistance: {max_call_oi}"
            #     resistance_status = "str_resistance"
                
                
            support_status = "str_support"
             # For puts, check if a valid second put exists and then determine support status
            if second_put_category is not None:
                # Find the indices in the original put_oi list
                max_index = put_oi.index(max_put_oi)
                second_index = put_oi.index(second_highest_put)
                # If the second-highest appears below the max cell (i.e. higher index), assign "wtt_support"
                # If it appears above the max cell (i.e. lower index), assign "wtb_support"
                if second_index > max_index:
                    support_status = "wtt_support"
                else:
                    support_status = "wtb_support"
            # else:
            #     # If no valid second put exists, then use the max put OI as support.
            #     # str_support = f"Max put OI support: {max_put_oi}"
            #     support_status = "str_support"


            
            trade_executed = sell_put_trade(resistance_status, support_status, market_ltp, weekly_range_support)
            if trade_executed:
                logger.info("Sell put trade executed successfully.")
            else:
                logger.info("Sell put trade conditions not met.")           


        except Exception as e:
            logger.error(f"Error during processing: {e}")
            print(f"Error: {e}")
    else:
        logger.info("Skipping initialization as the current time is not between 09:15 and 15:30.")









# if __name__ == "__main__":
#     # Open the workbook (replace with your actual file path)
#     wb_path = "option_chain.xlsm"  # Adjust the path to your Excel file
#     try:
#         wb = xw.Book(wb_path)

#         # Run the function
#         oi_change_extract(wb)
    
#     except Exception as e:
#         logger.error(f"Error opening the workbook: {e}")
#         print(f"Error opening the workbook: {e}")
    
