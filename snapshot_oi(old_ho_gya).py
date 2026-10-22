
#################################################? first way ####################################################
#? screen updating and intractive added of second code

import xlwings as xw
from datetime import datetime
import time
from sql.append_data_db import store_snapshot

# Specify your Excel file path
# excel_file_path = "option_chain.xlsm"

def append_snapshot_to_table(wb):
    # wb = xw.Book(excel_file_path)
    ws_source = wb.sheets['nifty']
    history_sheet = wb.sheets['nifty_snapshot_live']
    pivot_sheet = wb.sheets['snapshot_graph']  # Your pivot table sheet
    
    # Turn off interaction and screen updates
    wb.app.screen_updating = False
    wb.app.api.Interactive = False

    try:
        # Define the table in the target sheet
        table = history_sheet.api.ListObjects("nifty_snapshot_table")
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Fetch the data from the source sheet
        call_OI_snap = ws_source.range('M12:M26').value
        call_token_snap = ws_source.range('F12:F26').value
        put_token_snap = ws_source.range('AB12:AB26').value
        put_OI_snap = ws_source.range('U12:U26').value
        call_OI_chg_snap = ws_source.range('L12:L26').value
        put_OI_chg_snap = ws_source.range('V12:V26').value
        strike_price_snap = ws_source.range('Q12:Q26').value


        # Append data to the table
        for i in range(15):
            if call_token_snap[i] and call_OI_snap[i]:
                new_row = table.ListRows.Add()
                new_row.Range(1, 1).Value = timestamp
                new_row.Range(1, 2).Value = call_token_snap[i]
                new_row.Range(1, 3).Value = call_OI_snap[i]
                new_row.Range(1, 4).Value = call_OI_chg_snap[i]
                new_row.Range(1, 5).Value = strike_price_snap[i]
                new_row.Range(1, 6).Value = "call type"
                

            if put_token_snap[i] and put_OI_snap[i]:
                new_row = table.ListRows.Add()
                new_row.Range(1, 1).Value = timestamp
                new_row.Range(1, 2).Value = put_token_snap[i]
                new_row.Range(1, 3).Value = put_OI_snap[i]
                new_row.Range(1, 4).Value = put_OI_chg_snap[i]
                new_row.Range(1, 5).Value = strike_price_snap[i]
                new_row.Range(1, 6).Value = "put type"

                
        # Refresh Pivot Tables on the pivot sheet
        for pivot in pivot_sheet.api.PivotTables():
            pivot.PivotCache().Refresh()

        # Save the workbook
        # wb.save()
        print(f"Snapshot appended and pivot refreshed at {timestamp}")
        # store_snapshot()
    except Exception as e:
        print(f"Error during snapshot append: {e}")
    
    finally:
        # Always re-enable interaction and screen updating
        wb.app.api.Interactive = True
        wb.app.screen_updating = True




#?main.py me paste kr do

# import time
# from snapshot_oi import append_snapshot_to_table  # Import the function from the other script

# def run_snapshot_append():
#     while True:
#         try:
#             # Call the function to append snapshot
#             append_snapshot_to_table()
#             time.sleep(60)  # Wait for 60 seconds before running again
#         except Exception as loop_error:
#             print(f"Main Loop Error: {loop_error}")
#             time.sleep(60)  # Wait for 60 seconds before retrying in case of an error

# if __name__ == "__main__":
#     # Run the snapshot append function
#     run_snapshot_append()

#? Notes for above code

#* 💡 Important Notes:
#* Suppression only affects Excel UI, not your Python/WebSocket code.
#* It does not block incoming WebSocket data or interfere with networking.
#* It reduces OLE errors by locking Excel UI from being touched while writing.


################################################? second way ##################################################################

# import xlwings as xw
# from datetime import datetime
# import time

# # Path to the Excel file
# excel_file_path = "option_chain.xlsm"

# def append_snapshot_to_table():
#     try:
#         wb = xw.Book(excel_file_path)
#         ws_source = wb.sheets['nifty']
#         history_sheet = wb.sheets['nifty_snapshot_live']

#         # Access the Excel Table by name using the Excel COM API
#         table = history_sheet.api.ListObjects("nifty_OI_table")

#         # Read data from source sheet
#         call_OI_snap = ws_source.range('M12:M26').value
#         call_token_snap = ws_source.range('F12:F26').value
#         put_token_snap = ws_source.range('AB12:AB26').value
#         put_OI_snap = ws_source.range('U12:U26').value

#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         # Append each valid Token/OI pair as a row in the table
#         for i in range(15):
#             if call_token_snap[i] and call_OI_snap[i]:
#                 new_row = table.ListRows.Add()  # Adds a new blank row at the bottom
#                 new_row.Range(1, 1).Value = timestamp  # Column A (Timestamp)
#                 new_row.Range(1, 2).Value = call_token_snap[i]  # Column B (call_token_snap)
#                 new_row.Range(1, 3).Value = call_OI_snap[i]     # Column C (call_OI_snap)

#             if put_token_snap[i] and put_OI_snap[i]:
#                 new_row = table.ListRows.Add()
#                 new_row.Range(1, 1).Value = timestamp
#                 new_row.Range(1, 2).Value = put_token_snap[i]
#                 new_row.Range(1, 3).Value = put_OI_snap[i]

#         wb.save()
#         print(f"Snapshot appended at {timestamp}")

#     except Exception as e:
#         print(f"Error during snapshot append: {e}")


# #? Main.py calling
# def append_periodically():
#     while True:
#         try:
#             append_snapshot_to_table()
#             time.sleep(60)  # Wait 60 seconds before running the function again
#         except Exception as e:
#             print(f"Error in the main loop: {e}")
#             time.sleep(60)  # Wait 60 seconds before retrying


# if __name__ == "__main__":
#     # Run the snapshot append function
#     append_periodically()






















#? different thing generally append snapshot data rows by row in cells (not in excel table)

# import xlwings as xw
# from datetime import datetime
# import time

# excel_file_path = "option_chain.xlsm"

# def read_and_append_to_table():
#     wb = xw.Book(excel_file_path)
#     ws_source = wb.sheets['nifty']
#     ws_target = wb.sheets['nifty_snapshot_live']

#     # Get the Excel table in the target sheet (assumes only one table exists)
#     excel_table = ws_target.tables[0]  # Table that starts from A2

#     # Read data from source sheet
#     call_OI_snap = ws_source.range('M12:M26').value
#     call_token_snap = ws_source.range('F12:F26').value
#     put_token_snap = ws_source.range('AB12:AB26').value
#     put_OI_snap = ws_source.range('U12:U26').value

#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     # Combine data into rows for appending
#     combined_rows = []
#     for i in range(15):
#         if call_token_snap[i] and call_OI_snap[i]:
#             combined_rows.append([current_time, call_token_snap[i], call_OI_snap[i]])
#         if put_token_snap[i] and put_OI_snap[i]:
#             combined_rows.append([current_time, put_token_snap[i], put_OI_snap[i]])

#     # Find the next row in the table
#     table_range = excel_table.range
#     next_row = table_range.last_cell.row + 1

#     # Write data to the table starting from next_row
#     ws_target.range(f'A{next_row}').value = combined_rows

#     wb.save()
#     print(f"{len(combined_rows)} rows appended to table at {current_time}.")

# # Loop every minute
# while True:
#     try:
#         read_and_append_to_table()
#         time.sleep(60)  # Wait for 1 minute
#     except Exception as e:
#         print(f"Error: {e}")
#         time.sleep(60)  # Wait and try again













#? some more controler code for python
# # Refresh Pivot Tables
# for pivot in pivot_sheet.api.PivotTables():
#     pivot.PivotCache().Refresh()

# # Force refresh of all charts
# for chart in pivot_sheet.api.ChartObjects():
#     chart.Chart.Refresh()

# # Run VBA macro to reapply colors
# wb.app.api.Run("ApplyPivotChartColors")

#? to ensures correct color applying to line graphs


# Sub ApplyPivotChartColors()
#     Dim cht As ChartObject
#     Dim s1 As Series
#     Dim s2 As Series
#     Dim maxSeries As Series
#     Dim minSeries As Series

#     ' Loop through all charts in the sheet
#     For Each cht In ActiveSheet.ChartObjects
#         If cht.Chart.SeriesCollection.Count = 2 Then ' Ensure two tokens exist
#             Set s1 = cht.Chart.SeriesCollection(1)
#             Set s2 = cht.Chart.SeriesCollection(2)

#             ' Get max & min series
#             If Application.WorksheetFunction.Max(s1.Values) > Application.WorksheetFunction.Max(s2.Values) Then
#                 Set maxSeries = s1
#                 Set minSeries = s2
#             Else
#                 Set maxSeries = s2
#                 Set minSeries = s1
#             End If

#             ' Apply colors
#             maxSeries.Format.Line.ForeColor.RGB = RGB(255, 0, 0) ' Red for higher value
#             minSeries.Format.Line.ForeColor.RGB = RGB(0, 176, 80) ' Green for lower value
#         End If
#     Next cht
# End Sub
