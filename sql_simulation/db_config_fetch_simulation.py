import os
import sys
import time
from datetime import datetime
import pandas as pd

# Add parent directory to sys.path for importing get_workbook
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from get_workbook_simulation import wb, current_dir


def load_db_config_simulation():
    credential = wb.sheets['credential']
    sheet = wb.sheets['snap_nifty']

    # Extract and clean values from Excel
    host = str(credential.range("b15").value).strip()
    user = str(credential.range("b16").value).strip()
    password = str(credential.range("b17").value).strip()
    port = str(int(credential.range("b18").value)).strip()


    # Safely handle None for SSL certificate path
    ssl_ca_relative = credential.range("b19").value
    # print(ssl_ca_relative, type(ssl_ca_relative))
    
    
    ssl_ca_relative = str(ssl_ca_relative) if ssl_ca_relative else "" # Convert to empty string if None   
    # print(ssl_ca_relative, type(ssl_ca_relative))
    
    ssl_chosen = bool(credential.range("b20").value)
    ssl_ca_path = os.path.join(current_dir, ssl_ca_relative) if ssl_ca_relative else None


    #? selecting database
    selected_date = sheet.range('F1').value
    print(selected_date, type(selected_date))
    if selected_date:
        try:
            selected_date = pd.to_datetime(selected_date).date()
        except Exception as e:
            print("Invalid expiry format in Excel. Using today's date.", e)
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    # MySQL Configuration
    database_name = f"market_{selected_date}"

    # Build the connection config
    db_config = {
        "host": host,
        "user": user,
        "password": password,
        "database": database_name,
        "port": port
    }

    if ssl_chosen:
        if ssl_ca_path:
            db_config["ssl_ca"] = ssl_ca_path
        else:
            print("Warning: SSL is enabled, but no SSL certificate path is provided.")
   
    return db_config


# === Module-level global ===
db_config = load_db_config_simulation()

# Uncomment if needed for debugging:
print(db_config)

