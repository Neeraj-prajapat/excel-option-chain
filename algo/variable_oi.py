
from percentage_variable import categorize_ratio, var_75, var_80, var_85, var_90, var_95

def variable_oi_call(call_oi, max_call_oi, max_index_call):
    
    sorted_call_oi = sorted(call_oi, reverse=True)
    second_highest_call = sorted_call_oi[1]
    second_index_call = call_oi.index(second_highest_call) 
    
    second_call_category = None
    if second_highest_call:
        ratio_call = second_highest_call / max_call_oi
        cat_call = categorize_ratio(ratio_call)
        if cat_call in [var_75, var_80, var_85, var_90, var_95]:
            second_call_category = cat_call
    
    resistance_status = "str_resistance"
    if second_call_category is not None:
        if second_index_call > max_index_call:
            resistance_status = "wtt_resistance"
        else:
            resistance_status = "wtb_resistance"
    return resistance_status, cat_call, second_index_call



def variable_oi_put(put_oi, max_put_oi, max_index_put):
    
    sorted_put_oi = sorted(put_oi, reverse=True)
    second_highest_put = sorted_put_oi[1]
    second_index_put = put_oi.index(second_highest_put) 
    
    second_put_category = None
    if second_highest_put:
        ratio_put = second_highest_put / max_put_oi
        cat_put = categorize_ratio(ratio_put)
        if cat_put in [var_75, var_80, var_85, var_90, var_95]:
            second_put_category = cat_put
    
    resistance_status = "str_resistance"
    if second_put_category is not None:
        if second_index_put > max_index_put:
            resistance_status = "wtt_resistance"
        else:
            resistance_status = "wtb_resistance"
    return resistance_status, cat_put, second_index_put
