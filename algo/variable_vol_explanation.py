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
    if resistance_status == "wtt_resistance" and (support_status == "wtt_support" or support_status == "str_support"):
        # if abs(market_ltp - weekly_bottom) / weekly_bottom <= threshold:
        if abs(market_ltp - weekly_bottom)  <= max_diff:
            print("Trade Conditions Met:")
            # Insert your trade API call here to execute a sell put trade
            print("Executing SELL PUT trade...")
            return True
    return False

def algo(wb):
    current_time = datetime.now().time()
    start_time = datetime.strptime("09:15", "%H:%M").time()
    cutoff_time = datetime.strptime("15:30", "%H:%M").time()
    
    if current_time > start_time and current_time < cutoff_time:
        ws_source = wb.sheets['nifty']
        try:
            call_volume = ws_source.range('N12:N26').value
            put_volume = ws_source.range('T12:T26').value
            
            weekly_range_support = ws_source.range('C5')
            weekly_range_resistance = ws_source.range('C4')
            market_ltp = ws_source.range('Q10')
            
            max_call_volume = max(call_volume)          
            max_put_volume = max(put_volume)            
            
            resistance = max_call_volume
            support = max_put_volume
            
            max_index_call = call_volume.index(max_call_volume)  
            max_index_put = put_volume.index(max_put_volume)  
            
            sorted_call_volume = sorted(call_volume, reverse=True)
            sorted_put_volume  = sorted(put_volume, reverse=True)
                      
            second_highest_call = sorted_call_volume[1] 
            second_highest_put  = sorted_put_volume[1] 
            
            second_index_put = put_volume.index(second_highest_put)
            second_index_call = call_volume.index(second_highest_put)
            
            second_call_category = None
            ratio_call = second_highest_call / max_call_volume
            cat_call = categorize_ratio(ratio_call)
            if cat_call in [var_75, var_80, var_85, var_90, var_95]:
                second_call_category = cat_call

            second_put_category = None
            ratio_put = second_highest_put / max_put_volume
            cat_put = categorize_ratio(ratio_put)
            if cat_put in [var_75, var_80, var_85, var_90, var_95]:
                second_put_category = cat_put

            
            resistance_status = "str_resistance"
            if second_call_category is not None:
                max_index = call_volume.index(max_call_volume)
                second_index = call_volume.index(second_highest_call)
                if second_index > max_index:
                    resistance_status = "wtt_resistance"
                else:
                    resistance_status = "wtb_resistance"
                
            support_status = "str_support"
            if second_put_category is not None:
                max_index = put_volume.index(max_put_volume)
                second_index = put_volume.index(second_highest_put)
                if second_index > max_index:
                    support_status = "wtt_support"
                else:
                    support_status = "wtb_support"
            


            
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
#         volume_change_extract(wb)
    
#     except Exception as e:
#         logger.error(f"Error opening the workbook: {e}")
#         print(f"Error opening the workbook: {e}")
    
