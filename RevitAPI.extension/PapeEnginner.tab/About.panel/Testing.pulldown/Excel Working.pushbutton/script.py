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

def Transpose(data):
    cleaned_data = []
    for sheet_data in data:
        sheet_rows = []
        for row in sheet_data:
            if isinstance(row, tuple):  # Nếu là tuple thì giữ nguyên
                sheet_rows.append(list(row))
            elif isinstance(row, list):  # Nếu là list thì mở rộng từng hàng
                for sub_row in row:
                    sheet_rows.append(list(sub_row))
        cleaned_data.append(sheet_rows)

    return cleaned_data


def ExportToExcel(sheet_titles, start_row, start_column, data):
    """
    Xuất dữ liệu ra file Excel với nhiều sheet.

    Args:
        sheet_titles (list): Danh sách tên các sheet.
        start_row (int): Dòng bắt đầu ghi dữ liệu.
        start_column (int): Cột bắt đầu ghi dữ liệu.
        data (list): Danh sách dữ liệu cấp 3.
    """
    transposeData = Transpose(data)

    # Chọn nơi lưu file Excel
    file_path = forms.save_file(
        file_ext='xlsx',
        title='Chọn nơi lưu file Excel',
        default_name='ExportedData.xlsx'
    )

    if not file_path:
        print("Không có đường dẫn được chọn. Hủy thao tác.")
        return

    # Tạo ứng dụng Excel
    excel_app = Excel.ApplicationClass()
    excel_app.Visible = True  # Hiển thị Excel
    # excel_app.DisplayAlerts = False  # Tắt cảnh báo

    # Tạo workbook mới
    workbook = excel_app.Workbooks.Add()

    # Kiểm tra danh sách sheet và dữ liệu có khớp không
    if len(sheet_titles) != len(data):
        Alert("Lỗi: Số lượng sheet không khớp với số lượng data.")
        return

    # Xóa các sheet mặc định nếu có
    while workbook.Sheets.Count > 1:
        workbook.Sheets(1).Delete()

    # print("So luong sheet duoc tao:", len(sheet_titles))
    # print("Data Input:")
    for i, d in enumerate(transposeData):
        print(50 * "-")
        print("Sheet {}: {}".format(sheet_titles[i], d))

    # Duyệt qua từng sheet
    for sheet_index, sheet_name in enumerate(sheet_titles):
        # Tạo sheet mới
        if sheet_index >= workbook.Sheets.Count:
            worksheet = workbook.Sheets.Add(After=workbook.Sheets(workbook.Sheets.Count))
        else:
            worksheet = workbook.Sheets(sheet_index + 1)

        # Đặt tên sheet (giới hạn 31 ký tự)
        worksheet.Name = sheet_name[:31]

        # Lấy dữ liệu cho sheet hiện tại
        sheet_data = transposeData[sheet_index]
        # print(50*"-")
        # print(sheet_data)

        #     # Kiểm tra dữ liệu có hợp lệ không
        #     if not isinstance(sheet_data, list) or not isinstance(sheet_data[0], list):
        #         print("Loi: Du lieu '{}' khong hop le".format(sheet_name))
        #         continue
        #
        # Ghi tiêu đề cột
        worksheet.Cells(start_row, start_column).Value2 = "Family"
        worksheet.Cells(start_row, start_column + 1).Value2 = "Type"
        worksheet.Cells(start_row, start_column + 2).Value2 = "ID"

        # Ghi dữ liệu vào từng hàng & cột
        for row_idx, row_data in enumerate(sheet_data, start=start_row + 1):
            for col_idx, value in enumerate(row_data):
                worksheet.Cells(row_idx, start_column + col_idx).Value2 = value

    # Lưu workbook
    workbook.SaveAs(file_path)

    # Đóng workbook và Excel để giải phóng bộ nhớ
    # workbook.Close(SaveChanges=False)
    # excel_app.Quit()

    # Giải phóng bộ nhớ
    # del workbook
    # del excel_app

    # # Hiển thị thông báo hoàn thành
    # forms.alert(
    #     message="Dữ liệu đã được xuất thành công!",
    #     title="Xuất dữ liệu thành công",
    #     exitscript=True
    # )

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

