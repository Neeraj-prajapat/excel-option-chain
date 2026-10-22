def manage_nifty_snapshot_table(wb):
    """Manages the 'nifty_snapshot_table' sheet in the workbook, backs up data, and recreates the table."""

    from datetime import datetime
    import pandas as pd
    import logging

    logger = logging.getLogger(__name__)

    # Get the current time
    current_time = datetime.now().time()

    # Define the allowed time window (9:00 AM - 9:20 PM)
    start_time = datetime.strptime("09:00", "%H:%M").time()
    cutoff_time = datetime.strptime("09:20", "%H:%M").time()

    if start_time <= current_time < cutoff_time:
        if "nifty_snapshot_live" not in [s.name for s in wb.sheets]:
            history_sheet = wb.sheets.add("nifty_snapshot_live")
        else:
            history_sheet = wb.sheets["nifty_snapshot_live"]

        # Check if table exists
        try:
            table = history_sheet.api.ListObjects("nifty_snapshot_table")
            table_exists = True
        except:
            table_exists = False

        if table_exists:
            try:
                # data_range = table.DataBodyRange                                                                  #? you can be removed this block of code if you don't want to store backup      
                # if data_range is not None:
                #     data = data_range.Value
                #     df = pd.DataFrame(data, columns=["Timestamp", "Token", "OI", "OI Change", "Strike Price", "type"])

                #     backup_date = datetime.now().strftime("%Y-%m-%d")
                #     backup_filename = f"backup_nifty_oi_snap/nifty_snapshot_backup_{backup_date}.csv"

                #     if not df.empty:
                #         df.to_csv(backup_filename, index=False)
                #         logger.info(f"Table data backed up to {backup_filename}.")
                #     else:
                #         logger.info("Table data is empty, no backup created.")

                table.Delete()
                logger.info("Deleted the entire table 'nifty_snapshot_table'.")

            except Exception as e:
                logger.error(f"Error managing table: {e}")
                history_sheet.clear()
                logger.info("Cleared the entire sheet content.")

        # Recreate table with headers
        history_sheet.range("A1").value = ["Timestamp", "Token", "OI", "OI Change", "Strike Price", "type"]

        try:
            new_table = history_sheet.api.ListObjects.Add(
                1,  # xlSrcRange
                history_sheet.range("A1:F1").api,
                None,
                1   # xlYes (has headers)
            )
            new_table.Name = "nifty_snapshot_table"
            logger.info("Successfully created table 'nifty_snapshot_table' with headers.")

        except Exception as e:
            logger.error(f"Failed to create table: {e}")

    else:
        logger.info("Skipping 'nifty_snapshot_live' initialization as the current time is outside 9:00 AM - 9:20 PM.")
