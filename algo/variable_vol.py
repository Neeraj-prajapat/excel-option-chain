from percentage_variable import categorize_ratio, var_75, var_80, var_85, var_90, var_95

def variable_vol_call(call_vol, max_call_vol, max_index_call):
    
    sorted_call_vol = sorted(call_vol, reverse=True)
    second_highest_call = sorted_call_vol[1]
    second_index_call = call_vol.index(second_highest_call) 
    
    second_call_category = None
    if second_highest_call:
        ratio_call = second_highest_call / max_call_vol
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



def variable_vol_put(put_vol, max_put_vol, max_index_put):
    
    sorted_put_vol = sorted(put_vol, reverse=True)
    second_highest_put = sorted_put_vol[1]
    second_index_put = put_vol.index(second_highest_put) 
    
    second_put_category = None
    if second_highest_put:
        ratio_put = second_highest_put / max_put_vol
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
