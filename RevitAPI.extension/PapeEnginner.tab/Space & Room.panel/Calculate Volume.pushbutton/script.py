#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

""" ----------------------FUNCTIONS----------------------------"""


def GetTotalVolume(lstEles):
    totalVolumeFt3 = float(0)

    for ele in lstEles:
        if ele.Category.Name == "Spaces" or ele.Category.Name == "Rooms":
            volumeParam = ele.LookupParameter("Volume")  # Lấy tham số Volume
            if volumeParam and volumeParam.HasValue:
                totalVolumeFt3 += volumeParam.AsDouble()  # Thêm giá trị thể tích vào tổng (ft³)

    # Chuyển đổi từ ft³ sang m³
    totalVolumeM3 = totalVolumeFt3 * 0.0283168466

    # Chuyển đổi sang m³/h (giả sử tính toán theo giờ)
    totalVolumeM3H = totalVolumeM3  # (giữ nguyên nếu không có thêm bước nào)

    return totalVolumeM3H


""" ----------------------MAIN CODE----------------------------"""

try:
    selection = uidoc.Selection.GetElementIds()

    if not selection:
        TaskDialog.Show("Error", "There is no eleements to choose")
    else:
        lstEle = [doc.GetElement(e) for e in selection]
        totalVolume = GetTotalVolume(lstEle)

        # Hiển thị tổng thể tích
        if totalVolume > 0:
            TaskDialog.Show("Total Volume", "The total volume of selected spaces is {:.2f} m³/h".format(totalVolume))
        else:
            TaskDialog.Show("Total Volume", "No spaces with volume were found in the selection.")


except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
