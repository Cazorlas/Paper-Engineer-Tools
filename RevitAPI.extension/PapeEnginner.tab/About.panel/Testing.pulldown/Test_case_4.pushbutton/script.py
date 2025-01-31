# -*- coding: utf-8 -*-

# import clr
# import System
#
# clr.AddReference('Microsoft.Office.Interop.Excel')
# from Microsoft.Office.Interop import Excel
#
# def open_new_excel():
#     # Tạo một ứng dụng Excel mới
#     excel_app = Excel.ApplicationClass()
#     excel_app.Visible = True  # Hiển thị Excel
#
#     # Tạo một workbook mới
#     workbook = excel_app.Workbooks.Add()
#
#     # Chọn sheet đầu tiên
#     worksheet = workbook.Worksheets[1]
#
#     # Ghi giá trị vào ô A1
#     worksheet.Range["A1"].Value2 = "Hello, PyRevit!"
#
#     # Không đóng workbook để người dùng có thể sử dụng
#     # workbook.Close(False)
#
#     # Không cần gọi excel_app.Quit() vì ta đang mở một file mới
#
# # Gọi hàm để khởi tạo Excel
# open_new_excel()


import clr
import System

clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
from pyrevit import forms

def save_excel_file():
    # Chọn đường dẫn lưu file trước
    filepath = forms.save_file(
        file_ext='xlsx',
        title='Chọn nơi lưu file Excel',
        default_name='NewExcelFile.xlsx'
    )

    if not filepath:
        print("Không có đường dẫn được chọn. Hủy thao tác.")
        return

    # Tạo một ứng dụng Excel mới
    excel_app = Excel.ApplicationClass()
    excel_app.Visible = True  # Hiển thị Excel

    # Tạo một workbook mới
    workbook = excel_app.Workbooks.Add()
    worksheet = workbook.Worksheets[1]

    # Ghi giá trị vào ô A1
    worksheet.Range["A1"].Value2 = "Hello, PyRevit!"

    # Lưu workbook vào đường dẫn đã chọn
    workbook.SaveAs(filepath)



    # Không đóng workbook để người dùng có thể tiếp tục chỉnh sửa
    # workbook.Close(False)
    # excel_app.Quit()

# Gọi hàm để chọn đường dẫn và lưu Excel
save_excel_file()

