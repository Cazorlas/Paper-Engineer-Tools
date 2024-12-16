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


def CollectLinkData():
    """
    Collect all required data about Revit links in the model.
    """
    refLinkInstance = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    linkType = [doc.GetElement(ref.GetTypeId()) for ref in refLinkInstance]
    externalFileRef = [link.GetExternalFileReference() for link in linkType]
    docLink = [ref.GetLinkDocument() for ref in refLinkInstance]

    #
    pathName = [
        ModelPathUtils.ConvertModelPathToUserVisiblePath(i.GetAbsolutePath()) for i in externalFileRef
    ]
    #
    nameLink = [link.LookupParameter("Type Name").AsString() for link in linkType]
    #
    statusLoad = ["Loaded" if i is not None else "Not Loaded" for i in docLink]
    #
    linkWorkset = []
    for link in refLinkInstance:
        worksetId = link.WorksetId
        worksetTable = doc.GetWorksetTable()
        workset = worksetTable.GetWorkset( worksetId)
        linkWorkset.append(workset)
    linkWorksetName = [i.Name for i in linkWorkset]
    #
    referenceType = [
        "Overlay" if hasattr(link, "AttachmentType") and link.AttachmentType == AttachmentType.Overlay
        else "Attachment" if hasattr(link, "AttachmentType")
        else "Unknown"
        for link in linkType
    ]
    #
    worksetCollector = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    worksetName = [i.Name for i in worksetCollector] if worksetCollector else ["Not a working share file"]

    return nameLink, statusLoad, pathName, linkWorksetName, worksetName


"""----------------------MAIN CODE----------------------------"""

try:

    """------------RUN FORM----------"""
    openForm = True
    while openForm:
        # Thu thập dữ liệu ban đầu
        nameLink, statusLoad, pathName, linkWorksetName, worksetName = CollectLinkData()

        # Mở form với dữ liệu hiện tại
        f = MainForm(nameLink, statusLoad, pathName, linkWorksetName, worksetName)
        f.ShowDialog()

        # User cancel
        if f.DialogResult != System.Windows.Forms.DialogResult.OK:
            break

        elif f.DialogResult == System.Windows.Forms.DialogResult.OK:
            # Cập nhật lại dữ liệu từ Revit model sau khi thực hiện thay đổi
            nameLink, statusLoad, pathName, linkWorksetName, worksetName = CollectLinkData()
            openForm = False





# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass


# Handle any other exceptions and show an error message
except Exception as ex:
    ShowNotification("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
