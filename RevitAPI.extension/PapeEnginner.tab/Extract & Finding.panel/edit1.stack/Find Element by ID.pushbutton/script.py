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


def ZoomAllElement(document, lstEleId, linkSelected):
    """Zoom all Element. I will not use it for now"""

    validElements = []
    for elemId in lstEleId:
        elem = document.GetElement(elemId)  # document here could be "doc" or "doclink"
        if elem and hasattr(elem, "get_BoundingBox") and elem.get_BoundingBox(None):
            validElements.append(elem)

    if not validElements:
        ShowNotification("Warning", "No valid elements found with BoundingBox.")

    # Gộp BoundingBox
    firstBox = validElements[0].get_BoundingBox(None)
    bboxMin = firstBox.Min
    bboxMax = firstBox.Max

    for elem in validElements[1:]:
        bbox = elem.get_BoundingBox(None)
        if bbox:
            bboxMin = XYZ(
                min(bboxMin.X, bbox.Min.X),
                min(bboxMin.Y, bbox.Min.Y),
                min(bboxMin.Z, bbox.Min.Z),
            )
            bboxMax = XYZ(
                max(bboxMax.X, bbox.Max.X),
                max(bboxMax.Y, bbox.Max.Y),
                max(bboxMax.Z, bbox.Max.Z),
            )

    if not bboxMin or not bboxMax:
        ShowNotification("Warning", "No valid BoundingBox found for selected elements.")

    transform = linkSelected.GetTotalTransform()
    try:
        globalPoint1 = transform.OfPoint(bboxMin)
        globalPoint2 = transform.OfPoint(bboxMax)

        # Sử dụng hàm isFinite để kiểm tra tính hợp lệ
        if not (isFinite(globalPoint1.X) and isFinite(globalPoint1.Y) and isFinite(
                globalPoint1.Z) and
                isFinite(globalPoint2.X) and isFinite(globalPoint2.Y) and isFinite(globalPoint2.Z)):
            raise ValueError("Invalid BoundingBox values detected.")

        uiview.ZoomAndCenterRectangle(globalPoint1, globalPoint2)
    except Exception as ex:
        ShowNotification("Error", "Zoom failed due to invalid BoundingBox: {}".format(ex))


# Define utility function
def isFinite(value):
    """Kiểm tra xem giá trị có phải là số hợp lệ (finite) hay không."""
    if value is None:
        return False
    if isinstance(value, (float, int)):
        return not (math.isnan(value) or math.isinf(value))
    return False


def SelectLinkELementById(docLink, linkSelected, lstEleId):
    """
        Select elements in the linked file based on a list of IDs.

        Parameters:
        :param docLink: Document of the linked file.
        :param linkSelected: RevitLinkInstance representing the linked file.
        :param lstEleId: List of ElementIds to select.
    """

    selReferences = []
    for eleId in lstEleId:
        try:
            eleLink = docLink.GetElement(eleId)

            if eleLink:
                reference = Reference(eleLink).CreateLinkReference(linkSelected)
                selReferences.append(reference)

        except Exception as ex:
            ShowNotification("Error", "No Element with ID {}\n{}".format(eleId, ex))

    if selReferences:
        selection.SetReferences(selReferences)


"""----------------------MAIN CODE----------------------------"""

try:

    collectModelLink = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

    # Get linked model elements and their names
    modelLink = [link for link in collectModelLink]
    nameModelLink = [link.Name for link in modelLink] if modelLink else ["There is no Link Model"]

    """------------RUN FORM----------"""
    openForm = True
    while openForm:
        f = MainForm(nameModelLink)
        f.Show()

        # User cancel
        if f.DialogResult != System.Windows.Forms.DialogResult.OK:
            break

        elif f.DialogResult == System.Windows.Forms.DialogResult.OK:

            radioLinkModel = f._linkBtn.Checked
            radioInModel = f._modelBtn.Checked

            lstId = f._textBox1.Text.strip().split(",")
            lstId = list(set(lstId))

            lstEleId = [ElementId(int(id.strip())) for id in lstId]
            lstEle = [doc.GetElement(id) for id in lstEleId]
            lstICollection = List[ElementId](lstEleId)

            linkModel = f._comboBox1.Text

            if radioInModel:
                lstEle, lstNoEle, lstName = FilterElementExistant(doc, lstEleId)

                if not lstEle:
                    ShowNotification("Warning", "No elements found with the given IDs.")
                    continue


                else:
                    ShowDataForm(doc, lstEleId)
                    selection.SetElementIds(lstICollection)
                    openForm = False



            elif radioLinkModel:

                if linkModel == "There is no Link Model":
                    ShowNotification("Warning", "There is no Link Model, please select a valid option.")
                    continue
                else:
                    # Tìm liên kết được chọn
                    linkSelected = next((link for link in modelLink if link.Name == linkModel), None)

                    # Lấy Document của file liên kết
                    docLink = linkSelected.GetLinkDocument()

                    lstEle, lstNoEle, lstName = FilterElementExistant(docLink, lstEleId)

                    # Hiển thị thông báo nếu không tìm thấy phần tử nào
                    if not lstEle:
                        ShowNotification("Warning", "No elements found with the given IDs.")
                        continue


                    else:
                        ShowDataForm(docLink, lstEleId)
                        SelectLinkELementById(docLink, linkSelected, lstEleId)
                        openForm = False



# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass


# Handle any other exceptions and show an error message
except Exception as ex:
    ShowNotification("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
