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
    """
    Update the "DP Space Name" and "DP Space Number" parameters of a given FamilyInstance based on the associated space.

    Args:
        ele (FamilyInstance): The Revit element to update.

    Returns:
        tuple: Count of successful and failed updates.
    """
    countSuccess = 0
    countFail = 0

    with Transaction(doc, "Update Space Info") as t:
        t.Start()
        try:
            if isinstance(ele, FamilyInstance):
                # space = ele.get_Space()
                point = ele.Location.Point
                space = doc.GetSpaceAtPoint(point)
                if space:
                    roomName = space.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                    roomNumber = space.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()

                    DPNameSpace = ele.LookupParameter("DP Space Name")
                    DPNumberSpace = ele.LookupParameter("DP Space Number")

                    if DPNameSpace and roomName:
                        DPNameSpace.Set(roomName)
                    if DPNumberSpace and roomNumber:
                        DPNumberSpace.Set(roomNumber)

                    countSuccess += 1
                else:
                    countFail += 1
            else:
                countFail += 1

        except Exception:
            countFail += 1
        t.Commit()

    return countSuccess, countFail


def ShowTaskDialog(title="title", mainInstruction="MainInstruction", mainContent="MainContent", allowCancellation=True):
    """ShowDialog with TaskDialog Information"""
    dialog = TaskDialog(title)
    dialog.MainInstruction = mainInstruction
    dialog.MainContent = mainContent
    dialog.TitleAutoPrefix = False
    dialog.MainIcon = TaskDialogIcon.TaskDialogIconInformation
    dialog.CommonButtons = TaskDialogCommonButtons.Ok
    # dialog.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel
    dialog.AllowCancellation = allowCancellation
    dialog.FooterText = '<a href="{0}">{1}</a>'.format(
        "https://www.youtube.com/@paper.engineer", "Help")

    return dialog.Show()


"""----------------------MAIN CODE----------------------------"""
if __name__ == "__main__":
    try:
        # Category list to filter
        categoryList = ["Mechanical Equipment","Air Terminals","Duct Fittings", "Duct Accessories"]
        # Get instances of specified categories
        instances = GetAllInstancesInViewByCategories(categoryList)

        # Process to Update Parameter
        with TransactionGroup(doc, "Update Space Number and Space Name") as tg:
            tg.Start()
            countSuccess = 0  # count for success cases
            countFail = 0  # count for Fail cases
            for i in instances:
                success, fail = UpdateSpaceInfo(i)
                countSuccess += success
                countFail += fail
            tg.Assimilate()

        ShowTaskDialog(
            title="Notification Result",
            mainInstruction="Update Space Info Result",
            mainContent="Update Done for {} elements\nUpdate Fail for {} elements".format(countSuccess, countFail)
        )

    # Handle the case when the user cancels the operation
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        TaskDialog.Show("Canceled", "Operation was canceled by the user.")

    # Handle any other exceptions and show an error message
    except Exception as ex:
        TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
