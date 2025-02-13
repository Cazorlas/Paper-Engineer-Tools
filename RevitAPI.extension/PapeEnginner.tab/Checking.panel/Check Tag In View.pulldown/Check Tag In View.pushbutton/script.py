# -*- coding: utf-8 -*-
import sys

#  ©️ Copyright:
#  - This script belongs to Paper Engineer.
#  - If you appreciate my content, please give credit when using it.
#
#  Please contact to: trinhvutuanhung@gmail.com,
#  or visit: https://www.youtube.com/@paper.engineer
#  to get more information
#

# TODO: Import libraries and modules
import clr  # Common Language Runtime for .NET
import System
import json
import os
import math  # Standard Python math library

# Excel Libraary
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script, EXEC_PARAMS

from rpw.ui.forms import *
from MainForm import MainForm

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
import Revit  # Import Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager  # Document management in Revit
from RevitServices.Transactions import TransactionManager  # Transaction management

import System.Windows.Forms
from System.Windows.Forms import Application

# TODO: Prepare variables and input
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
view = doc.ActiveView
DB = Autodesk.Revit.DB
output = script.get_output()
version = int(app.VersionNumber)
selection = uidoc.Selection

# Đặt lệnh này NGAY SAU khi import System.Windows.Forms
Application.EnableVisualStyles()

""" ----------------------FUNCTIONS----------------------------"""


# Định nghĩa lớp MyOption để tạo danh sách checkbox với tên tùy chọn
class MyOption(forms.TemplateListItem):
    def __init__(self, orig_item, checked=False):
        """
        Gói một đối tượng (tên danh mục) vào danh sách checkbox.

        Args:
            orig_item (str): Tên danh mục
            checked (bool): Trạng thái ban đầu của checkbox (mặc định là False)

        """
        super(MyOption, self).__init__(orig_item, checked=checked)
        self.item = orig_item  # Lưu trữ danh mục ban đầu

    @property
    def name(self):
        return "{}".format(self.item)  # Hiển thị tên danh mục trong danh sách


def Flatten_lv3(lst):
    return [i for subLst in lst for i in subLst]


def Flatten_lv2(lst):
    return [subLst for subLst in lst]


def ToList(input):
    if isinstance(input, list):
        return input
    else:
        return [input]


def AllElementOfCategoryInView(chooseView, categoryName):
    categoryName = ToList(categoryName)
    allCategories = doc.Settings.Categories
    valid_cate = []
    alleles = []
    for cate in allCategories:
        for category in categoryName:
            if cate.Name == category:
                valid_cate.append(cate)

    for cate in valid_cate:
        alleles.append(FilteredElementCollector(doc, chooseView.Id).OfCategoryId(
            cate.Id).WhereElementIsNotElementType().ToElements())

    return Flatten_lv3(alleles)


def AllAnnotationCategories():
    allCategories = doc.Settings.Categories

    return [cat for cat in allCategories if cat.CategoryType == CategoryType.Annotation]


def GetTaggedElement(tag):
    result = []
    if version < 2022:
        taggedElement = tag.GetTaggedLocalElement()
        result.append(taggedElement)
    else:
        taggedElements = tag.GetTaggedLocalElements()
        for element in taggedElements:
            result.append(element)
    return result


def SetDifference(lst1, lst2):
    """lst 1 > lst2"""
    result = []
    for item1 in lst1:
        if item1 not in lst2:
            result.append(item1)
    return result


def GroupByKey(items, keys):
    # Create unique key lists
    unique_keys = []
    for key in keys:
        if key not in unique_keys:
            unique_keys.append(key)

    # Create empty lists according to unique keys
    group_lst = []
    for i in range(len(unique_keys)):
        group_lst.append([])

    # Get index of the input keys in unique key lists
    ind_lst = []
    for key in keys:
        ind_lst.append(unique_keys.index(key))

    # Group by key
    for item, ind in zip(items, ind_lst):
        group_lst[ind].append(item)

    return group_lst, unique_keys


def GetElementCategory(ele):
    return ele.Category.Name


def GetFamilyNameOfElement(ele):
    return ele.LookupParameter('Family').AsValueString()


def GetTypeNameOfElement(ele):
    return ele.Name


def ProcessCategoryTag(lstCate):
    result = []
    for cate in lstCate:
        getAll = AllElementOfCategoryInView(view, cate)
        if len(getAll) == 0:
            result.append(False)
        else:
            result.append(True)
    return result


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

    """----------------------MAIN CODE----------------------------"""


if __name__ == "__main__":
    try:
        global formInputInstance

        # Lấy config
        # config = script.get_config(EXEC_PARAMS.command_name)
        # previousSelectedCategories = config.get_option('selected_category', False)

        annotationCategories = AllAnnotationCategories()
        annotationCategoriesName = [cate.Name for cate in annotationCategories]
        annotationCategoriesDict = dict(zip(annotationCategoriesName, annotationCategories))
        sortedData = sorted(annotationCategoriesName)
        # sortedData = sorted(annotationCategoriesDict)

        # Lấy danh sách tùy chọn
        # ops = sorted(annotationCategoriesDict)
        # ops = [MyOption(cate, checked=cate in previousSelectedCategories) for cate in sortedData]

        # Run Setting first
        projectInfo = doc.ProjectInformation
        param = projectInfo.LookupParameter("checkTagConfiguration")

        if param is None:
            Alert(content="Please run Setting First", title="Warning", exit=True)
        else:
            paramValue = param.AsValueString()
            if not paramValue:
                Alert(content="Please run Setting First", title="Warning", exit=True)
            else:
                data = json.loads(paramValue)
                selectCateName = data.get('listViewItem', [])

                # selectCateName = forms.SelectFromList.show(
                #     {'Annotation Categories': ops},
                #     title='Select Categories',
                #     group_selector_title='Select Categories',
                #     multiselect=True
                # )
                #
                # if not selectCateName:
                #     Alert('No choose any category.', exit=True)
                # else:
                #
                #     config.selected_category = ToList(selectCateName)
                #     script.save_config()
                #
                #
                #
                processCateTag = ProcessCategoryTag(selectCateName)

                allTagOfCategoryInView = AllElementOfCategoryInView(view, selectCateName)
                taggedElement = Flatten_lv3([GetTaggedElement(tag) for tag in allTagOfCategoryInView])  # List 2

                cateNameOfTaggedElement = sorted(list(set([ele.Category.Name for ele in taggedElement])))
                allModelElement = AllElementOfCategoryInView(view, cateNameOfTaggedElement)  # List 1

                allEle = AllElementOfCategoryInView(view, selectCateName)

                """----------------------Compare and find elements have not been tagged----------------------------"""

                taggedElementId = [element.Id for element in taggedElement]
                modelElementId = [element.Id for element in allModelElement]

                notTaggedElementId = SetDifference(modelElementId, taggedElementId)
                notTaggedCategoryName = [doc.GetElement(id).Category.Name for id in notTaggedElementId]

                groupElementByCategory = GroupByKey(notTaggedElementId, notTaggedCategoryName)
                notTaggedElementGroup = groupElementByCategory[0]  # Get elements have been grouped
                notTaggedCategoryGroup = groupElementByCategory[1]

                taggedCategory = list(set(cateNameOfTaggedElement) - set(notTaggedCategoryGroup))

                try:
                    if len(allTagOfCategoryInView) == 0:
                        Alert('All Elements Have Not Been Tagged.', exit=True)
                    elif len(notTaggedCategoryGroup) > 0:
                        notTaggedCategory = [GetElementCategory(doc.GetElement(Id)) for Id in notTaggedElementId]
                        notTaggedFamilyRaw = [GetFamilyNameOfElement(doc.GetElement(Id)) for Id in notTaggedElementId]
                        notTaggedTypeRaw = [GetTypeNameOfElement(doc.GetElement(Id)) for Id in notTaggedElementId]
                        notTaggedIdRaw = [Id.IntegerValue for Id in notTaggedElementId]

                        groupFamily = GroupByKey(notTaggedFamilyRaw, notTaggedCategory)
                        notTaggedFamily = groupFamily[0]

                        groupType = GroupByKey(notTaggedTypeRaw, notTaggedCategory)
                        notTaggedType = groupType[0]

                        groupId = GroupByKey(notTaggedIdRaw, notTaggedCategory)
                        notTaggedId = groupId[0]

                        data = [[list(zip(family, typeName, ids))] if len(family) == 1 else [[(fam, typ, Id)] for
                                                                                             fam, typ, Id in
                                                                                             zip(family, typeName, ids)]
                                for
                                family, typeName, ids in zip(notTaggedFamily, notTaggedType, notTaggedId)]

                        """-----------RUN FORM-----------"""
                        f = MainForm(notTaggedCategory, notTaggedFamilyRaw, notTaggedTypeRaw, notTaggedIdRaw,
                                     processCateTag,
                                     selectCateName, notTaggedCategoryGroup, data)
                        # f.LoadData(notTaggedCategory, notTaggedFamilyRaw, notTaggedTypeRaw, notTaggedIdRaw)
                        Application.Run(f)

                        # ExportToExcel(notTaggedCategoryGroup, 1, 1, data)

                    if len(taggedCategory) != 0:
                        result = ", ".join(map(str, taggedCategory))
                        print('All Elements Of  {} Have Been Tagged.'.format(result))

                    # if processCateTag:
                    #     raw = ""
                    #     for bool, cate in zip(processCateTag, selectCateName):
                    #         if bool == False:
                    #             if raw == "":
                    #                 raw += cate
                    #             else:
                    #                 raw += ", " + cate
                    #     if raw == "":
                    #         pass
                    #     else:
                    #         print('Can not find any {} in view.'.format(raw))


                except Exception as exx:
                    TaskDialog.Show("Failed", "Warning: {}".format(exx))  # Corrected string formatting







    except Autodesk.Revit.Exceptions.OperationCanceledException:
        pass

    except Exception as ex:
        TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
