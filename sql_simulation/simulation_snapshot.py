
import mysql.connector
import time
from datetime import datetime
import pandas as pd
import xlwings as xw
from decimal import Decimal
from db_config_fetch_simulation import db_config
from get_workbook_simulation import wb


# Open Excel Workbook
# excel_file_path = "recorded_replay.xlsm"
# wb = xw.Book(excel_file_path)
sheet = wb.sheets['snap_nifty']

# # Get the selected expiry date from Excel (F1)
# selected_date = sheet.range('F1').value
# # print(selected_date)

# if selected_date:
#     try:
#         selected_date = pd.to_datetime(selected_date).date()
#     except Exception as e:
#         print("Invalid expiry format in Excel. Using today's date.", e)
#         selected_date = datetime.now().date()
# else:
#     selected_date = datetime.now().date()

# # MySQL Configuration
# database_name = f"market_{selected_date}"

# db_config = {
#     "host": "localhost",
#     "user": "Neeraj Prajapati",
#     "password": "Nneer@j870342sql",
#     "database": database_name,
#     "port": 3306
# }

def fetch_snapshots():
    """Fetch snapshots grouped by timestamp with 15 strikes each"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Get all data ordered by timestamp and strike price
        cursor.execute("""
            SELECT * FROM marketdata 
            ORDER BY SnapshotTime ASC, Strike_Price ASC
        """)
        
        # Group into 15-row chunks (1 timestamp = 15 strikes)
        all_data = cursor.fetchall()
        return [all_data[i:i+15] for i in range(0, len(all_data), 15)]
        
    except Exception as e:
        print("❌ Error fetching snapshots:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def convert_decimal(value):
    """Convert decimals to floats"""
    return float(value) if isinstance(value, Decimal) else value

def get_frame_duration():
    """Get playback speed from Excel"""
    try:
        return max(0.1, float(sheet.range("F2").value))
    except:
        return 1.0

def is_running():
    """Check playback control status"""
    return sheet.range("F3").value == "RUN"

# def play_snapshots():
#     """Main playback function with proper 15-row formatting"""
#     snapshot_batches = fetch_snapshots()
    
#     if not snapshot_batches:
#         print("⚠ No data found")
#         return

#     print(f"🎥 Loaded {len(snapshot_batches)} snapshots")
    
#     while True:
#         if not is_running():
#             time.sleep(1)
#             continue
            
#         frame_time = get_frame_duration()
#         print(f"▶ Playing {len(snapshot_batches)} snapshots ({frame_time}s/frame)")

#         for batch in snapshot_batches:
#             if not is_running():
#                 print("⏸ Playback stopped")
#                 return

#             # Convert all 15 rows for this timestamp
#             excel_rows = []
#             for db_row in batch:
#                 # Convert DB row to Excel format: skip ID (index 0)
#                 excel_row = [convert_decimal(value) for value in db_row[2:]]  # Skip ID and keep timestamp
#                 excel_rows.append(excel_row)
            
#             # Write to Excel as 15 rows x 23 columns
#             sheet.range("F12").value = excel_rows  # Writes 15 rows starting at F12
            
#             # Update timestamp display
#             if batch:
#                 timestamp = batch[0][1]  # Get timestamp from first row
#                 if isinstance(timestamp, str):
#                     timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#                 sheet.range("N10").value = f"Snapshot: {timestamp.strftime('%H:%M:%S')}"
            
#             time.sleep(frame_time)

#         print("✅ Replay complete. Press RUN to restart")

# # Start playback
# play_snapshots()




 #? 1. included more function to stop and replay where you left (i have not checked it yet)

# def play_snapshots():
#     """Pause-resume playback from last viewed snapshot batch"""
#     snapshot_batches = fetch_snapshots()
#     if not snapshot_batches:
#         print("⚠ No data found")
#         return

#     print(f"🎥 Loaded {len(snapshot_batches)} snapshots")

#     current_index = 0  # Track where we are in the batch list

#     while True:
#         if not is_running():
#             time.sleep(1)
#             continue

#         frame_time = get_frame_duration()
#         print(f"▶ Resuming from snapshot {current_index + 1}/{len(snapshot_batches)} ({frame_time}s/frame)")

#         while current_index < len(snapshot_batches):
#             if not is_running():
#                 print(f"⏸ Paused at snapshot {current_index + 1}")
#                 break  # Wait loop outside will handle pause

#             batch = snapshot_batches[current_index]

#             # Convert and write batch to Excel
#             excel_rows = [
#                 [convert_decimal(value) for value in db_row[2:]]
#                 for db_row in batch
#             ]
#             sheet.range("F12").value = excel_rows

#             # Show timestamp
#             timestamp = batch[0][1]
#             if isinstance(timestamp, str):
#                 timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#             sheet.range("N10").value = f"Snapshot: {timestamp.strftime('%H:%M:%S')}"

#             time.sleep(frame_time)
#             current_index += 1

#         if current_index >= len(snapshot_batches):
#             print("✅ Replay complete. Waiting for RUN to restart...")
#             current_index = 0  # Reset if full loop finishes


#? 2. included also from above:- not loop when when 1 day data ended

def play_snapshots():
    """Play snapshots, pause/resume, and exit after finishing all data"""
    snapshot_batches = fetch_snapshots()
    if not snapshot_batches:
        print("⚠ No data found")
        return

    print(f"🎥 Loaded {len(snapshot_batches)} snapshots")

    current_index = 0  # Track current position in the batch list

    while current_index < len(snapshot_batches):
        if not is_running():
            print(f"⏸ Paused at snapshot {current_index + 1}")
            time.sleep(1)
            continue

        frame_time = get_frame_duration()
        batch = snapshot_batches[current_index]

        # Convert and write batch to Excel
        excel_rows = [
            [convert_decimal(value) for value in db_row[2:]]
            for db_row in batch
        ]
        sheet.range("F12").value = excel_rows

        # Show timestamp
        timestamp = batch[0][1]
        if isinstance(timestamp, str):
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        sheet.range("N10").value = f"Snapshot: {timestamp.strftime('%H:%M:%S')}"

        time.sleep(frame_time)
        current_index += 1

    print("✅ Playback finished. Exiting.")

# Start playback
play_snapshots()