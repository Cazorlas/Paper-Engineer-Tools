#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import json  # Library để lưu và đọc file JSON
import os  # Library để thao tác với hệ thống file
import codecs
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

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

from pyrevit import EXEC_PARAMS

from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox, Alert

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

"""----------------------FUNCTION----------------------------"""


class SelectionFilter(ISelectionFilter):
    """Filter to select only elements of specific categories for UI selection."""

    def __init__(self, categoryNames):
        # categoryNames là một list các tên category (e.g., ["Ducts", "Duct Fittings"])
        self.categoryNames = categoryNames

    def AllowElement(self, element):
        if element.Category and element.Category.Name in self.categoryNames:
            return True
        return False

    def AllowReference(self, reference, point):
        return False


def GetAllInstancesInViewByCategories(categoryList):
    """
    Get all instances in the current view filtered by a list of category names.

    Args:
        categoryList (list): List of category names (e.g., ["Ducts", "Duct Fittings", "Duct Accessories"])

    Returns:
        list: List of elements that match the category criteria in the current view
    """
    # Lấy danh sách tất cả các category từ document
    categories = doc.Settings.Categories

    # Tạo danh sách các BuiltInCategory tương ứng với categoryList
    categoryIds = List[ElementId]()
    for categoryName in categoryList:
        for cat in categories:
            if cat.Name == categoryName:
                categoryIds.Add(cat.Id)
                break

    # Sử dụng ElementMulticategoryFilter để lọc theo danh sách category
    if categoryIds.Count > 0:
        multicategoryFilter = ElementMulticategoryFilter(categoryIds)
        filteredElements = FilteredElementCollector(doc, view.Id) \
            .WhereElementIsNotElementType() \
            .WherePasses(multicategoryFilter) \
            .ToElements()
    else:
        filteredElements = []  # Trả về danh sách rỗng nếu không tìm thấy category

    return list(filteredElements)


def UpdateSpaceInfo(ele):
    roomName = None  # Khởi tạo mặc định
    roomNumber = None

    with Transaction(doc, "Update Space Info") as t:
        t.Start()

        try:
            if isinstance(ele, FamilyInstance):
                # Lấy vị trí của FamilyInstance
                location = ele.Location
                if location and isinstance(location, LocationPoint):
                    point = location.Point

                    # Tìm Space tại vị trí đó
                    space = doc.GetRoomAtPoint(point)
                    if space:
                        roomName = space.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() or "N/A"
                        roomNumber = space.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() or "N/A"

                        # Lấy Parameter cần cập nhật
                        DPNameSpace = ele.LookupParameter("DP Space Name")
                        DPNumberSpace = ele.LookupParameter("DP Space Number")

                        # Cập nhật giá trị nếu Parameter tồn tại
                        if DPNameSpace and roomName:
                            DPNameSpace.Set(roomName)
                        if DPNumberSpace and roomNumber:
                            DPNumberSpace.Set(roomNumber)

        except Exception as ex:
            print("Failed to update element {}: {}".format(ele.Id, ex))

        t.Commit()

    return roomName, roomNumber  # Trả về giá trị, dù có hay không



"""----------------------MAIN CODE----------------------------"""
if __name__ == "__main__":
    try:
        # Ví dụ danh sách category bạn muốn lọc
        categoryList = ["Duct Fittings", "Duct Accessories"]
        # Gọi hàm để lấy các đối tượng
        instances = GetAllInstancesInViewByCategories(categoryList)

        lstA = []
        lstB = []

        with TransactionGroup(doc, "Update Space Number and Space Name") as tg:
            tg.Start()
            for i in instances:
                a,b = UpdateSpaceInfo(i)
                lstA.append(a)
                lstB.append(b)
            tg.Assimilate()

        print(lstA,lstB)

        # with TransactionGroup(doc, "Update Space Number and Space Name") as tg:
        #     tg.Start()
        #
        #     for i in instances:
        #         # UpdateSpaceInfo(i)
        #
        #     tg.Assimilate()

        # Alert("Update Done for {} elements".format(len(instances)), "Notification")





    # Handle the case when the user cancels the operation
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        TaskDialog.Show("Canceled", "Operation was canceled by the user.")

    # Handle any other exceptions and show an error message
    except Exception as ex:
        TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
