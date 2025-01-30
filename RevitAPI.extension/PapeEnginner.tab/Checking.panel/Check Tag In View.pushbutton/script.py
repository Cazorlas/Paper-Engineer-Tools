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
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script, EXEC_PARAMS

from rpw.ui.forms import *
import json

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

# TODO: Prepare variables and input
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
view = doc.ActiveView
DB = Autodesk.Revit.DB
output = script.get_output()
version = int(app.VersionNumber)
selection = uidoc.Selection
# Đường dẫn tới file lưu trữ lựa chọn
options_file = 'selected_options.json'

""" ----------------------FUNCTIONS----------------------------"""

# # Định nghĩa lớp MyOption để tạo các tùy chọn
# class MyOption(forms.TemplateListItem):
#     @property
#     def name(self):
#         return "Option: {}".format(self.item)
#
# # Đọc các lựa chọn đã chọn trước đó từ config
# def load_selected_options():
#     try:
#         # Lấy cấu hình của script
#         config = script.get_config(EXEC_PARAMS.command_name)
#         # Trả về danh sách các mục đã được chọn trong config
#         return config.get('selected_categories', [])
#     except Exception as ex:
#         print("Error reading the file: {}".format(ex))
#         return []
#
# # Lưu các lựa chọn vào config
# def save_selected_options(selected):
#     try:
#         # Lấy cấu hình của script
#         config = script.get_config(EXEC_PARAMS.command_name)
#         # Cập nhật giá trị cấu hình
#         config.set('selected_categories', selected)
#         # Lưu lại cấu hình
#         script.save_config(config)
#     except Exception as ex:
#         print("Error saving to config: {}".format(ex))
#
# # Lấy danh sách các tùy chọn và đánh dấu các tùy chọn đã chọn
# def get_options(annotationCategoriesDict):
#     ops = [MyOption(cate) for cate in annotationCategoriesDict]
#
#     # Đọc các tùy chọn đã chọn từ config (nếu có)
#     selected_options = load_selected_options()
#     for option in ops:
#         if option.item in selected_options:
#             option.checked = True  # Đánh dấu các mục đã chọn
#
#     return ops


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


def GroupByKey(items,keys):
    #Create unique key lists
    unique_keys = []
    for key in keys:
        if key not in unique_keys:
            unique_keys.append(key)

    #Create empty lists according to unique keys
    group_lst = []
    for i in range(len(unique_keys)):
        group_lst.append([])

    #Get index of the input keys in unique key lists
    ind_lst = []
    for key in keys:
        ind_lst.append(unique_keys.index(key))

    #Group by key
    for item, ind in zip(items,ind_lst):
        group_lst[ind].append(item)

    return group_lst,unique_keys

"""----------------------MAIN CODE----------------------------"""
try:
    # Lấy config
    # config = script.get_config(EXEC_PARAMS.command_name)

    annotationCategories = AllAnnotationCategories()
    annotationCategoriesName = [cate.Name for cate in annotationCategories]
    annotationCategoriesDict = dict(zip(annotationCategoriesName, annotationCategories))

    # Lấy danh sách tùy chọn
    ops = sorted(annotationCategoriesDict)

    # Select form
    selectCateName = forms.SelectFromList.show(
        {'Annotation Categories': ops},
        title='MultiGroup List',
        group_selector_title='Select Categories',
        multiselect=True
    )

    if not selectCateName:
        Alert('No Category Selected. Please Select Again', exit=True)



    allTagOfCategoryInView = AllElementOfCategoryInView(view, selectCateName)
    taggedElement = Flatten_lv3([GetTaggedElement(tag) for tag in allTagOfCategoryInView]) #List 2

    cateNameOfTaggedElement = sorted(list(set([ele.Category.Name for ele in taggedElement])))
    allModelElement = AllElementOfCategoryInView(view,cateNameOfTaggedElement) #List 1

    """----------------------Compare and find elements have not been tagged----------------------------"""

    taggedElementId = [element.Id for element in taggedElement]
    modelElementId = [element.Id for element in allModelElement]

    print(cateNameOfTaggedElement)
    print(50 * "-")
    print(allModelElement)



except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
