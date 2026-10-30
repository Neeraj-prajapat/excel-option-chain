import xlwings as xw
import logging
from datetime import datetime
import math
from variable_oi import variable_oi_call, variable_oi_put
from variable_vol import variable_vol_call, variable_vol_put
from variable_oi_vol import variable_mix_call, variable_mix_put

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def variable(wb):
    current_time = datetime.now().time()
    start_time = datetime.strptime("09:15", "%H:%M").time()
    cutoff_time = datetime.strptime("15:30", "%H:%M").time()
    
    if current_time > start_time and current_time < cutoff_time:
        ws_source = wb.sheets['nifty']
        try:
            # Fetch data from Excel columns M (M12:M26) and U (U12:U26)
            call_oi = ws_source.range('M12:M26').value
            put_oi = ws_source.range('U12:U26').value
            
            call_vol = ws_source.range('N12:N26').value
            put_vol = ws_source.range('T12:T26').value
            
            strike_price = ws_source.range('Q12:Q26').value
            
            weekly_range_support = ws_source.range('C5')
            weekly_range_resistance = ws_source.range('C4')
            market_ltp = ws_source.range('Q10')
            
             # Round up market_ltp to the nearest multiple of 50
            nifty_atm = math.ceil(market_ltp / 50) * 50
            index_atm = strike_price.index(nifty_atm)
            
            max_call_oi = max(call_oi)           
            max_put_oi = max(put_oi)            
            
            max_call_vol = max(call_vol)          
            max_put_vol = max(put_vol)            
            
            # resistance = max_call_oi
            # support = max_put_oi
            
            # Initialize resistance and support positions
            max_index_call_oi = call_oi.index(max_call_oi)   
            max_index_put_oi = put_oi.index(max_put_oi)  
            
            max_index_call_vol = call_vol.index(max_call_vol)  
            max_index_put_vol = put_vol.index(max_put_vol)
            
            # Calculate the absolute difference between index_atm and the indices of max values
            distance_call_oi = abs(max_index_call_oi - index_atm)
            distance_put_oi = abs(max_index_put_oi - index_atm)
            distance_call_vol = abs(max_index_call_vol - index_atm)
            distance_put_vol = abs(max_index_put_vol - index_atm)
            
            if distance_call_vol < distance_call_oi:
                variable_vol_call()
            elif distance_call_vol > distance_call_oi:
                variable_oi_call()
            else:
                variable_mix_call()
                
            if distance_put_vol < distance_put_oi:
                variable_vol_put()
            elif distance_put_vol > distance_put_oi:
                variable_oi_put()
            elif distance_put_vol == distance_put_oi:
                variable_mix_put()

                


        except Exception as e:
            logger.error(f"Error during processing: {e}")
            print(f"Error: {e}")
    else:
        logger.info("Skipping initialization as the current time is not between 09:15 and 15:30.")