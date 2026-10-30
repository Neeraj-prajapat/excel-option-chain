from percentage_variable import categorize_ratio, var_75, var_80, var_85, var_90, var_95

def variable_mix_call(call_oi, max_call_oi, index_atm,  max_call_vol, call_vol, max_index_call_vol, max_index_call_oi):
        
    resistance_status = "str_resistance"
    
    # Process for call_vol
    sorted_call_vol = sorted(call_vol, reverse=True)
    second_highest_call_vol = sorted_call_vol[1]
    second_index_call_vol = call_vol.index(second_highest_call_vol)
    
    second_call_category_vol = None
    if second_highest_call_vol:
        ratio_call_vol = second_highest_call_vol / max_call_vol
        cat_call_vol = categorize_ratio(ratio_call_vol)
        if cat_call_vol in [var_75, var_80, var_85, var_90, var_95]:
            second_call_category_vol = cat_call_vol
    
    # Process for call_oi
    sorted_call_oi = sorted(call_oi, reverse=True)
    second_highest_call_oi = sorted_call_oi[1]
    second_index_call_oi = call_oi.index(second_highest_call_oi)
    
    second_call_category_oi = None
    if second_highest_call_oi:
        ratio_call_oi = second_highest_call_oi / max_call_oi
        cat_call_oi = categorize_ratio(ratio_call_oi)
        if cat_call_oi in [var_75, var_80, var_85, var_90, var_95]:
            second_call_category_oi = cat_call_oi
    
    # Determine resistance status based on the distance between indices and categories
    distance_call_vol = abs(second_index_call_vol - index_atm)
    distance_call_oi = abs(second_index_call_oi - index_atm)

    both_second_jaade = second_index_call_vol < max_index_call_vol and second_index_call_oi < max_index_call_oi
    
    if second_call_category_vol is not None and second_call_category_oi is not None:
        if second_index_call_vol < max_index_call_vol or second_index_call_oi < max_index_call_oi or both_second_jaade:
            resistance_status = "wtb_resistance"
        elif second_index_call_vol > max_index_call_vol and second_index_call_oi > max_index_call_oi:
            resistance_status = "wtt_resistance"
    
    # Default to "str_resistance" if no valid categories are found
    return resistance_status, cat_call_vol, second_index_call_vol


# if second_index_call_vol > max_index_call_vol or second_index_call_oi > max_index_call_oi or  both_second_jaade:
#         resistance_status = "wtt_support"
#     elif second_index_call_vol < max_index_call_vol and second_index_call_oi < max_index_call_oi:
#         resistance_status = "wtb_support"


def variable_mix_put(put_oi, max_put_oi, index_atm,  max_put_vol, put_vol, max_index_put_vol, max_index_put_oi):
        
    suppport_status = "str_support"
    
    # Process for put_vol
    sorted_put_vol = sorted(put_vol, reverse=True)
    second_highest_put_vol = sorted_put_vol[1]
    second_index_put_vol = put_vol.index(second_highest_put_vol)
    
    second_put_category_vol = None
    if second_highest_put_vol:
        ratio_put_vol = second_highest_put_vol / max_put_vol
        cat_put_vol = categorize_ratio(ratio_put_vol)
        if cat_put_vol in [var_75, var_80, var_85, var_90, var_95]:
            second_put_category_vol = cat_put_vol
    
    # Process for put_oi
    sorted_put_oi = sorted(put_oi, reverse=True)
    second_highest_put_oi = sorted_put_oi[1]
    second_index_put_oi = put_oi.index(second_highest_put_oi)
    
    second_put_category_oi = None
    if second_highest_put_oi:
        ratio_put_oi = second_highest_put_oi / max_put_oi
        cat_put_oi = categorize_ratio(ratio_put_oi)
        if cat_put_oi in [var_75, var_80, var_85, var_90, var_95]:
            second_put_category_oi = cat_put_oi
    
    # Determine resistance status based on the distance between indices and categories
    distance_put_vol = abs(second_index_put_vol - index_atm)
    distance_put_oi = abs(second_index_put_oi - index_atm)

    both_second_jaade = second_index_put_vol > max_index_put_vol and second_index_put_oi > max_index_put_oi
    
    if second_put_category_vol is not None and second_put_category_oi is not None:
        if second_index_put_vol > max_index_put_vol or second_index_put_oi > max_index_put_oi or  both_second_jaade:
                support_status = "wtt_support"   
            elif second_index_put_vol < max_index_put_vol and second_index_put_oi < max_index_put_oi:
                support_status = "wtb_support"
    
    # Default to "str_resistance" if no valid categories are found
    return support_status, cat_put_vol, second_index_put_vol