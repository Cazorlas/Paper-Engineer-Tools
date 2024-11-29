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

from SubForm import *

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


def SumBoxes(boundingBoxes, offset):
    """
    Calculate the sum of BoundingBoxXYZ.
    Parameters:
    - boundingBoxes: List of BoundingBoxXYZ.
    Returns:
    - BoundingBoxXYZ that contains the sum of all input BoundingBoxes.
    """

    minX = min([b.Min.X for b in boundingBoxes]) - offset
    minY = min([b.Min.Y for b in boundingBoxes]) - offset
    minZ = min([b.Min.Z for b in boundingBoxes]) - offset
    maxX = max([b.Max.X for b in boundingBoxes]) + offset
    maxY = max([b.Max.Y for b in boundingBoxes]) + offset
    maxZ = max([b.Max.Z for b in boundingBoxes]) + offset
    bb = BoundingBoxXYZ()
    bb.Min = XYZ(minX, minY, minZ)
    bb.Max = XYZ(maxX, maxY, maxZ)
    return bb


def GetSumBoundingBox(references, offset=1):
    """
    Calculate the sum of BoundingBoxXYZ from a list of References.
    Parameters:
    - references: List of References of the elements.
    Returns:
    - Summed BoundingBoxXYZ.
    """
    boundingBoxes = []
    for ref in references:
        # Get the element from the Reference
        element = doc.GetElement(ref.ElementId)

        # Check if it is a RevitLinkInstance
        if isinstance(element, RevitLinkInstance):
            transform = element.GetTotalTransform()
            linkedDoc = element.GetLinkDocument()
            linkedElement = linkedDoc.GetElement(ref.LinkedElementId)

            # Apply Transform to the BoundingBox
            bbx = linkedElement.get_BoundingBox(None)
            bbx.Min = transform.OfPoint(bbx.Min)
            bbx.Max = transform.OfPoint(bbx.Max)
            boundingBoxes.append(bbx)
        else:
            # If it is an element in the current Revit file
            bbx = element.get_BoundingBox(None)
            boundingBoxes.append(bbx)

    # Calculate the sum of the BoundingBox
    return SumBoxes(boundingBoxes, offset)


def Create3dView(doc, viewName):
    """
    Create a new 3D View in the current Revit document or reuse an existing one with the same name.
    Parameters:
    - doc: The current Revit document.
    - viewName: The name of the 3D view to create or reuse.
    Returns:
    - The View3D created or reused.
    """
    # Check if a 3D view with the same name already exists
    existingView = next(
        (v for v in FilteredElementCollector(doc).OfClass(View3D).ToElements() if v.Name == viewName),
        None
    )
    if existingView:
        return existingView  # Reuse the existing view

    # Get the 3D view family type
    viewFamily3d = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    viewFamily3d = next((v for v in viewFamily3d if v.ViewFamily == ViewFamily.ThreeDimensional), None)

    if not viewFamily3d:
        raise Exception("Cannot find ViewFamilyType for 3D View.")

    # Create a new 3D view
    with Transaction(doc, "Create 3D View") as t:
        t.Start()
        view3d = View3D.CreateIsometric(doc, viewFamily3d.Id)
        view3d.Name = viewName  # Set the name of the new view
        t.Commit()

    return view3d


"""----------------------MAIN CODE----------------------------"""

try:
    # Get the list of References from the current selection
    references = selection.GetReferences()

    if not references:
        ShowNotification("Error", "No Selection Element")

    else:

        # Calculate the sum of BoundingBox from the References
        sumBox = GetSumBoundingBox(references)

        # Specify the name for the 3D view
        viewName = "3D Elements View"

        # Create 3D View
        if view.ViewType == ViewType.ThreeD:
            view3d = view
        else:
            view3d = Create3dView(doc, viewName)

        # Set the SectionBox
        with Transaction(doc, "Set SectionBox") as t:
            t.Start()
            view3d.SetSectionBox(sumBox)
            t.Commit()

        # Switch to the 3D View after completing the transaction
        uidoc.RequestViewChange(view3d)
        uidoc.RefreshActiveView()
        # If you want to Zoom to Element. Activate the line below
        # uiview.ZoomAndCenterRectangle(sumBox.Min, sumBox.Max)


except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

# Handle any other exceptions and show an error message
except Exception as ex:
    ShowNotification("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
