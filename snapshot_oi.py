
#? this page is newer version of snapshot_oi(old_ho_gya).py (came bz adding new function store_snapshot() so, we are modifing to reduce time of excel interaction)
#################################################? first way ####################################################
#? screen updating and intractive added of second code

import xlwings as xw
from datetime import datetime
import time
from sql.append_data_db import store_snapshot

# Specify your Excel file path
file_path = "option_chain.xlsm"
wb = xw.Book(file_path)

def append_snapshot_to_table(wb):
    # wb = xw.Book(excel_file_path)
    ws_source = wb.sheets['nifty']
    history_sheet = wb.sheets['nifty_snapshot_live']
    pivot_sheet = wb.sheets['snapshot_graph']  # Your pivot table sheet
    data_block = ws_source.range("F12:AB26").value
    
    # Turn off interaction and screen updates
    wb.app.screen_updating = False
    wb.app.api.Interactive = False

    try:
        # Define the table in the target sheet
        table = history_sheet.api.ListObjects("nifty_snapshot_table")
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # # Fetch the data from the source sheet
        # call_OI_snap = ws_source.range('M12:M26').value
        # call_token_snap = ws_source.range('F12:F26').value
        # put_token_snap = ws_source.range('AB12:AB26').value
        # put_OI_snap = ws_source.range('U12:U26').value
        # call_OI_chg_snap = ws_source.range('L12:L26').value
        # put_OI_chg_snap = ws_source.range('V12:V26').value
        # strike_price_snap = ws_source.range('Q12:Q26').value


        # # Append data to the table
        # for i in range(15):
        #     if call_token_snap[i] and call_OI_snap[i]:
        #         new_row = table.ListRows.Add()
        #         new_row.Range(1, 1).Value = timestamp
        #         new_row.Range(1, 2).Value = call_token_snap[i]
        #         new_row.Range(1, 3).Value = call_OI_snap[i]
        #         new_row.Range(1, 4).Value = call_OI_chg_snap[i]
        #         new_row.Range(1, 5).Value = strike_price_snap[i]
        #         new_row.Range(1, 6).Value = "call type"
                

        #     if put_token_snap[i] and put_OI_snap[i]:
        #         new_row = table.ListRows.Add()
        #         new_row.Range(1, 1).Value = timestamp
        #         new_row.Range(1, 2).Value = put_token_snap[i]
        #         new_row.Range(1, 3).Value = put_OI_snap[i]
        #         new_row.Range(1, 4).Value = put_OI_chg_snap[i]
        #         new_row.Range(1, 5).Value = strike_price_snap[i]
        #         new_row.Range(1, 6).Value = "put type"

         # Iterate through each row in the data block
        for i in range(len(data_block)):
            # Extract needed values by index:
            call_token = data_block[i][0]      # Column F
            call_OI    = data_block[i][7]      # Column M
            call_OI_chg = data_block[i][6]      # Column L
            strike_price = data_block[i][11]    # Column Q
            put_OI     = data_block[i][15]     # Column U
            put_OI_chg = data_block[i][16]     # Column V
            put_token  = data_block[i][22]     # Column AB
            
            # Append row for call type if data exists
            if call_token and call_OI:
                new_row = table.ListRows.Add()
                new_row.Range(1, 1).Value = timestamp
                new_row.Range(1, 2).Value = call_token
                new_row.Range(1, 3).Value = call_OI
                new_row.Range(1, 4).Value = call_OI_chg
                new_row.Range(1, 5).Value = strike_price
                new_row.Range(1, 6).Value = "call type"
            
            # Append row for put type if data exists
            if put_token and put_OI:
                new_row = table.ListRows.Add()
                new_row.Range(1, 1).Value = timestamp
                new_row.Range(1, 2).Value = put_token
                new_row.Range(1, 3).Value = put_OI
                new_row.Range(1, 4).Value = put_OI_chg
                new_row.Range(1, 5).Value = strike_price
                new_row.Range(1, 6).Value = "put type"
                
        # Refresh Pivot Tables on the pivot sheet
        for pivot in pivot_sheet.api.PivotTables():
            pivot.PivotCache().Refresh()

        # Save the workbook
        # wb.save()
        print(f"Snapshot appended and pivot refreshed at {timestamp}")
    except Exception as e:
        print(f"Error during snapshot append: {e}")
    
    finally:
        # Always re-enable interaction and screen updating
        wb.app.api.Interactive = True
        wb.app.screen_updating = True

    store_snapshot(data_block)
    
    



#?main.py me paste kr do

# import time
# from snapshot_oi import append_snapshot_to_table  # Import the function from the other script

def run_snapshot_append():
    while True:
        try:
            # Call the function to append snapshot
            append_snapshot_to_table(wb)
            time.sleep(60)  # Wait for 60 seconds before running again
        except Exception as loop_error:
            print(f"Main Loop Error: {loop_error}")
            time.sleep(60)  # Wait for 60 seconds before retrying in case of an error

if __name__ == "__main__":
    # Run the snapshot append function
    run_snapshot_append()

#? Notes for above code

#* 💡 Important Notes:
#* Suppression only affects Excel UI, not your Python/WebSocket code.
#* It does not block incoming WebSocket data or interfere with networking.
#* It reduces OLE errors by locking Excel UI from being touched while writing.

