
import mysql.connector
import xlwings as xw
import schedule
import time
from datetime import datetime
from sql.db_config_fetch import db_config

# print(db_config)

# db_config = {
#     "host": str(credential.range("b15").value).strip(),  # Server URL    
#     "user": str(credential.range("b16").value).strip(),  
#     "password": str(credential.range("b17").value).strip(),  
#     "port": str(int(credential.range("b18").value)).strip(),
#     "ssl_ca": str(credential.range("b19").value).strip(),
#     "ssl_disabled": bool(credential.range("b20").value)
# }

# Generate database name with the current date
current_date = datetime.now().strftime("%Y-%m-%d")
database_name = f"market_{current_date}"

def create_database_and_table():
    """Creates the database and table if they don't exist."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        conn.database = database_name
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS marketdata (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            SnapshotTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            Call_token DECIMAL(18,2),
            Call_Vega DECIMAL(18,2),
            Call_theta DECIMAL(18,2),
            Call_gamma DECIMAL(18,2),
            Call_delta DECIMAL(18,2),
            Call_IV DECIMAL(18,2),
            Call_OI_Chg DECIMAL(18,2),
            Call_OI DECIMAL(18,2),
            Call_VOLUME DECIMAL(18,2),
            Call_LTP_CHG DECIMAL(18,2),
            Call_LTP DECIMAL(18,2),
            Strike_Price DECIMAL(18,2),
            Put_LTP DECIMAL(18,2),
            Put_LTP_CHG DECIMAL(18,2),
            Put_VOLUME DECIMAL(18,2),
            Put_OI DECIMAL(18,2),
            Put_OI_Chg DECIMAL(18,2),
            Put_IV DECIMAL(18,2),
            Put_delta DECIMAL(18,2),
            Put_gamma DECIMAL(18,2),
            Put_theta DECIMAL(18,2),
            Put_Vega DECIMAL(18,2),
            Put_token DECIMAL(18,2)            
        );
        """
        cursor.execute(create_table_query)
        print(f"✅ Database '{database_name}' and table 'marketdata' are ready.")
    except mysql.connector.Error as e:
        print(f"❌ Error creating database/table: {e}")
    finally:
        cursor.close()
        conn.close()

def store_snapshot(data_block):
    """Stores Excel snapshot in MySQL."""
    try:
        # Attempt connection to check if database exists
        conn = mysql.connector.connect(**db_config, database=database_name)
    except mysql.connector.Error:
        print("⚠️ Database not found, creating now...")
        create_database_and_table()
        conn = mysql.connector.connect(**db_config, database=database_name)  # Reconnect after creation
    
    try:
        cursor = conn.cursor()
        
        # Open Excel Workbook
        # file_path = "option_chain.xlsm"
        # wb = xw.Book(file_path)
        # ws_source = wb.sheets["nifty"]
        # data = ws_source.range("L12:V26").value
        
        cleaned_data = [
            [float(value) if isinstance(value, (int, float)) else 0.0 for value in row]
            for row in data_block
        ]
        
        insert_query = """
        INSERT INTO marketdata (
            Call_token, Call_Vega, Call_theta, Call_gamma, Call_delta, Call_IV, Call_OI_Chg, Call_OI, Call_VOLUME, Call_LTP_CHG, Call_LTP, 
            Strike_Price, Put_LTP, Put_LTP_CHG, Put_VOLUME, Put_OI, Put_OI_Chg, Put_IV, Put_delta, Put_gamma, Put_theta, Put_Vega, Put_token
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for row in cleaned_data:
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        print("✅ Snapshot saved to MySQL.")
    except Exception as e:
        print("❌ Error storing snapshot:", e)
    finally:
        cursor.close()
        conn.close()

# # Schedule snapshot every 10 seconds
# schedule.every(10).seconds.do(store_snapshot)

# # Run the scheduled tasks
# while True:
#     schedule.run_pending()
#     time.sleep(1)



















