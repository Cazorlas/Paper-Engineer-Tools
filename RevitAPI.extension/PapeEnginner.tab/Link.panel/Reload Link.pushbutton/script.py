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

uiviews = uidoc.GetOpenUIViews()
uiview = [x for x in uiviews if x.ViewId == view.Id][0]

# ------Note: __revit__ = Autodesk.Revit.UI.UIApplication
"""----------------------FUNCTION----------------------------"""

"""----------------------MAIN CODE----------------------------"""

try:
    # Thu thập các RevitLinkInstance
    refLinkInstance = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

    # Danh sách lưu thông tin
    pathName = []
    nameLink = []
    statusLoad = []
    referenceType = []
    workset = []

    for ref in refLinkInstance:
        # Lấy RevitLinkType từ RevitLinkInstance
        linkType = doc.GetElement(ref.GetTypeId())

        docLink = ref.GetLinkDocument()

        pathName.append(docLink.PathName if docLink is not None else "Unknown Path")

        # Lấy tên liên kết
        nameLink.append(linkType.LookupParameter("Type Name").AsString())

        # Trạng thái tải
        statusLoad.append("Loaded" if docLink is not None else "Unloaded")

        # Worsket
        workset.append(linkType.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM))

        # Loại tham chiếu (Reference Type: Overlay/Attachment)
        if hasattr(linkType, "AttachmentType"):
            referenceType.append("Overlay" if linkType.AttachmentType == AttachmentType.Overlay else "Attachment")
        else:
            referenceType.append("Unknown")

    # Hiển thị thông tin

    print("Path Names: ", pathName)
    print("-" * 50)
    print("Names: ", nameLink)
    print("-" * 50)
    print("Statuses: ", statusLoad)
    print("-" * 50)
    print("Reference Types: ", referenceType)
    print("-" * 50)
    print("Workset: ", workset)

    # targetFolder = forms.pick_folder()
    # if targetFolder:
    #     for ref in refLinkInstance:
    #         eleLink = doc.GetElement(ref.GetTypeId())

    f = MainForm()
    f.ShowDialog()




# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass


# Handle any other exceptions and show an error message
except Exception as ex:
    ShowNotification("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
