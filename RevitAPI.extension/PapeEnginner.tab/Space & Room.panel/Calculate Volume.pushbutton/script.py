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


def GetVolumes(lstEles):
    totalRoomVolumeFt3 = 0.0
    totalSpaceVolumeFt3 = 0.0

    for ele in lstEles:
        if ele.Category.Name == "Rooms":
            volumeParam = ele.LookupParameter("Volume")  # Lấy tham số Volume
            if volumeParam and volumeParam.HasValue:
                totalRoomVolumeFt3 += volumeParam.AsDouble()  # Thêm giá trị thể tích vào tổng (ft³)
        elif ele.Category.Name == "Spaces":
            volumeParam = ele.LookupParameter("Volume")
            if volumeParam and volumeParam.HasValue:
                totalSpaceVolumeFt3 += volumeParam.AsDouble()

    # Chuyển đổi từ ft³ sang m³
    totalRoomVolumeM3 = totalRoomVolumeFt3 * 0.0283168466
    totalSpaceVolumeM3 = totalSpaceVolumeFt3 * 0.0283168466

    return totalRoomVolumeM3, totalSpaceVolumeM3


def ShowTaskDialog(title, mainInstruction, icon, mainContent, footerText, footerUrl):
    # Tạo TaskDialog
    dialog = TaskDialog(title)
    dialog.TitleAutoPrefix = False
    dialog.MainInstruction = mainInstruction
    dialog.MainIcon = icon
    dialog.MainContent = mainContent
    dialog.CommonButtons = TaskDialogCommonButtons.Ok
    dialog.MainIcon = TaskDialogIcon.TaskDialogIconInformation

    # Kích hoạt thanh tiến trình kiểu marquee
    # dialog.EnableMarqueeProgressBar = True

    # Định dạng FooterText với thẻ <a> và gán vào FooterText
    dialog.FooterText = '<a href="{0}">{1}</a>'.format(footerUrl, footerText)

    # Hiển thị TaskDialog và nhận kết quả

    return dialog.Show()


""" ----------------------MAIN CODE----------------------------"""

try:
    selection = uidoc.Selection.GetElementIds()

    if not selection:
        TaskDialog.Show("Error", "There are no elements to choose")
    else:
        lstEle = [doc.GetElement(e) for e in selection]
        totalRoomVolume, totalSpaceVolume = GetVolumes(lstEle)

        # Hiển thị tổng thể tích
        if totalRoomVolume > 0 or totalSpaceVolume > 0:
            ShowTaskDialog(
                title="Paper Engineer",
                mainInstruction="Total Volume",
                icon=TaskDialogIcon.TaskDialogIconInformation,
                mainContent="Rooms: {:.2f} m³\nSpaces: {:.2f} m³".format(totalRoomVolume, totalSpaceVolume),
                footerText="Get help",
                footerUrl="https://www.youtube.com/@paper.engineer"
            )
        else:
            ShowTaskDialog(
                title="Paper Engineer",
                mainInstruction="Total Volume",
                icon=TaskDialogIcon.TaskDialogIconInformation,
                mainContent="No rooms or spaces with volume were found in the selection.",
                footerText="Get help",
                footerUrl="https://www.youtube.com/@paper.engineer"
            )

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    ShowTaskDialog(
        title="Paper Engineer",
        mainInstruction="Warning",
        icon=TaskDialogIcon.TaskDialogIconWarning,
        mainContent="Warning: {}".format(ex),
        footerText="Get help",
        footerUrl="https://www.youtube.com/@paper.engineer"
    )
