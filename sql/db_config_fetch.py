import os
import sys

# Add parent directory to sys.path for importing get_workbook
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from get_workbook import wb, current_dir


def load_db_config():
    credential = wb.sheets['credential']

    # Extract and clean values from Excel
    host = str(credential.range("b15").value).strip()
    user = str(credential.range("b16").value).strip()
    password = str(credential.range("b17").value).strip()
    port = str(int(credential.range("b18").value)).strip()

    # Safely handle None for SSL certificate path
    ssl_ca_relative = credential.range("b19").value
    print(ssl_ca_relative, type(ssl_ca_relative))
    
    
    ssl_ca_relative = str(ssl_ca_relative) if ssl_ca_relative else "" # Convert to empty string if None   
    print(ssl_ca_relative, type(ssl_ca_relative))
    
    ssl_disabled = credential.range("b20").value
    ssl_ca_path = os.path.join(current_dir, ssl_ca_relative) if ssl_ca_relative else None

    # Build the connection config
    db_config = {
        "host": host,
        "user": user,
        "password": password,
        "port": port
    }

    # Smart SSL handling
    if ssl_disabled:
        db_config["ssl_disabled"] = True
    elif ssl_ca_path:
        db_config["ssl_ca"] = ssl_ca_path
    else:
        print("Warning: SSL is enabled, but no SSL certificate path is provided.")

    return db_config


# === Module-level global ===
db_config = load_db_config()

# Uncomment if needed for debugging:
# print(db_config)



# if ssl_ca_relative:
#     ssl_ca_relative = str(ssl_ca_relative)             "None"    #? "Apple"
# else:
#     ssl_ca_relative = ""








#?nested if and else
#? above if and elif else part and this part is same in all scenario output

# if ssl_disabled:
#     # SSL is disabled, no need for certificate path
#     db_config["ssl_disabled"] = True
# else:
#     # SSL is enabled, so check for the certificate path
#     if ssl_ca_path:
#         # If certificate path is provided, use it
#         db_config["ssl_ca"] = ssl_ca_path
#     else:
#         # If certificate path is missing, print a warning
#         print("Warning: SSL is enabled, but no SSL certificate path is provided.")






# def load_db_config():
    
#     credential = wb.sheets['credential']
#     ssl_ca_path = os.path.join(current_dir, credential.range("b19").value.strip())
    
#     return{
#         "host":         str(credential.range("b15").value).strip(),
#         "user":         str(credential.range("b16").value).strip(),
#         "password":     str(credential.range("b17").value).strip(),
#         "port":         str(int(credential.range("b18").value)).strip(),
#         "ssl_ca":       ssl_ca_path,
#         "ssl_disabled": bool(credential.range("b20").value)
#     }
    
# # === Module‐level global ===
# # This code runs exactly once when Python imports config.py
# db_config = load_db_config()

# # print(db_config)
