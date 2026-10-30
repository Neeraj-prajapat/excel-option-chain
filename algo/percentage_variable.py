
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