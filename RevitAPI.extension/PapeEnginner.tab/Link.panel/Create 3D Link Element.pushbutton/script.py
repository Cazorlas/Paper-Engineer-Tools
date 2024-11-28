#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

from MainForm import *
from SubForm import *

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


def FilterElementExistant(document, lstEleId):
    """Filter List Element Existent or List Element non-Existent"""
    lstEle = []
    lstNoEle = []

    for id in lstEleId:

        ele = document.GetElement(id)
        if ele:
            lstEle.append(ele)
        else:
            lstNoEle.append(id)

    lstName = [e.Name for e in lstEle]

    return lstEle, lstNoEle, lstName


def SumBoxes(boxes):
    minx = min([b.Min.X for b in boxes])
    miny = min([b.Min.Y for b in boxes])
    minz = min([b.Min.Z for b in boxes])
    maxx = max([b.Max.X for b in boxes])
    maxy = max([b.Max.Y for b in boxes])
    maxz = max([b.Max.Z for b in boxes])
    bb = BoundingBoxXYZ()
    bb.Min = XYZ(minx, miny, minz)
    bb.Max = XYZ(maxx, maxy, maxz)
    return bb


def Create3DViewForSelection(references):
    viewType = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements().Find(
        lambda x: x.ViewFamily == ViewFamily.ThreeDimensional)

    for ref in references:
        linkInstance = doc.GetElement(ref)


        transform = linkInstance.GetTotalTransform()
        docLink = linkInstance.GetLinkDocument()
        eleLink = docLink.GetElement(ref.LinkedElementId)
        lstEle.append(eleLink)
        box = lstEle.get_BoundingBox(None)






"""----------------------MAIN CODE----------------------------"""

try:
    references = selection.GetReferences()

    # lstEle = [doc.GetElement(ref) for ref in references]



    bbx,elemInLinks=[],[]

    lstEle = []
    for ref in references:
        element = doc.GetElement(ref)
        # Kiểm tra nếu là RevitLinkInstance
        if isinstance(element, RevitLinkInstance):
            pass
        else:
            # Nếu không phải RevitLinkInstance, kiểm tra tài liệu chứa phần tử
            elementDoc = element.Document
            if elementDoc != doc:
                # Xác định RevitLinkInstance chứa file liên kết
                linkInstance = next(
                    (link for link in FilteredElementCollector(doc).OfClass(RevitLinkInstance)
                     if link.GetLinkDocument() == elementDoc),
                    None
                )
                linkName = linkInstance.Name if linkInstance else "Unknown Linked File"

            else:
                # Nếu thuộc tài liệu hiện tại
                pass








# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

# Handle any other exceptions and show an error message
except Exception as ex:
    ShowNotification("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
