import xlwings as xw
import os


# Internal cache
_wb = None
current_dir = os.path.dirname(os.path.realpath(__file__))

def get_workbook():
    global _wb
    if _wb is None:
        print("Workbook loaded ✅ (only once)")
        excel_file_path = os.path.join(current_dir, "option_chain.xlsm")
        _wb = xw.Book(excel_file_path)
    return _wb

# Expose workbook object once — ready for direct import
wb = get_workbook()





