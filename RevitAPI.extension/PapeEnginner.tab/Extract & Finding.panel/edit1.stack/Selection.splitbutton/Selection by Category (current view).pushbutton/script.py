#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

from SubForm import *
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

# Prepare document and other variables
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)
selection = uidoc.Selection

# ------Note: __revit__ = Autodesk.Revit.UI.UIApplication

"""----------------------FUNCTIONS----------------------------"""


def GetAllCategory():
    """
    Trả về danh sách tất cả các Category trong tài liệu Revit hiện tại.
    """
    categories = doc.Settings.Categories
    lstCategory = []
    lstCategoryName = []


    for category in categories:
        # Kiểm tra nếu category hợp lệ và thuộc kiểu Model
        if category and category.CategoryType == CategoryType.Model:
            lstCategory.append(category)
            lstCategoryName.append(category.Name)


    return lstCategory, lstCategoryName

def GetCategories(categories, categoriesName, selectedCategoriesName):
    """
    Lọc danh mục đã chọn từ danh sách categories và categoriesName.
    """
    lstCategories = []
    for selectedName in selectedCategoriesName:
        for i, name in enumerate(categoriesName):
            if selectedName == name:
                lstCategories.append(categories[i])
    return lstCategories

def SelectElementsByCategory(selectedCategories):
    """
    Chọn các phần tử trong view hiện tại dựa trên danh sách Category được tick.
    """
    selectedElements = []
    for category in selectedCategories:
        if category:
            collector = FilteredElementCollector(doc, view.Id)\
                .OfCategoryId(category.Id)\
                .WhereElementIsNotElementType()\
                .ToElements()
            selectedElements.extend(collector)


    if selectedElements:
        selection.SetElementIds(List[ElementId]([e.Id for e in selectedElements]))
    else:
        ShowNotification("Error","Can not find any Elements")





"""----------------------MAIN CODE----------------------------"""

try:
    # Ví dụ sử dụng
    categories, categoriesName = GetAllCategory()



    """------------RUN FORM----------"""
    openForm = True
    while openForm:

        # Mở form với dữ liệu hiện tại
        f = MainForm(categoriesName)
        f.ShowDialog()

        # Lấy danh mục đã chọn
        selectedCategoriesName = [item.Text for item in f._listView.Items if item.Checked]
        selectedCategories = GetCategories(categories, categoriesName, selectedCategoriesName)
        a = [i.Id for i in selectedCategories]


        # User cancel
        if f.DialogResult != System.Windows.Forms.DialogResult.OK:
            break

        elif f.DialogResult == System.Windows.Forms.DialogResult.OK:
            # print(a)

            # Gọi hàm để chọn các phần tử trong view dựa trên danh sách tick
            SelectElementsByCategory(selectedCategories)
            openForm = False

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
