#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
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


def SetWorkset(askWorkset, ele):
    """
    Đặt workset cho một element cụ thể
    """
    # Lấy danh sách tất cả Workset
    worksetCollector = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    selectedWorksetId = None

    # Tìm Workset ID dựa trên tên được chọn
    for workset in worksetCollector:
        if workset.Name == askWorkset:
            selectedWorksetId = workset.Id.IntegerValue
            break

    # Nếu không tìm thấy Workset, thông báo lỗi
    if selectedWorksetId is None:
        TaskDialog.Show("Error", "Workset '{}' not found.".format(askWorkset))
        return

    # Bắt đầu giao dịch để đặt Workset cho element
    with Transaction(doc, 'Set Workset') as t:
        t.Start()
        param = ele.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)

        if param and param.IsReadOnly == False:
            param.Set(selectedWorksetId)
        else:
            TaskDialog.Show("Error", "Cannot set Workset for element ID: {}".format(ele.Id))
        t.Commit()


"""----------------------MAIN CODE----------------------------"""

try:
    # Người dùng chọn các phần tử trong mô hình
    refEle = uidoc.Selection.PickObjects(ObjectType.Element, "Pick Objects")
    getEle = [doc.GetElement(e.ElementId) for e in refEle]

    # Lấy danh sách tất cả Workset
    worksetCollector = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    worksetName = [i.Name for i in worksetCollector]

    # Kiểm tra nếu không có Workset nào
    if not worksetName:
        TaskDialog.Show("Error", "No worksets available in the model.")
    else:
        # Yêu cầu người dùng chọn Workset
        askWorkset = forms.ask_for_one_item(
            worksetName,
            default=worksetName[0] if worksetName else None,
            prompt='Choose Workset',
            title='Please select a workset'
        )
        # Áp dụng Workset cho từng phần tử đã chọn
        with TransactionGroup(doc,'Set Workset for All') as tg:
            tg.Start()
            for e in getEle:
                SetWorkset(askWorkset, e)
            tg.Assimilate()

# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
