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


class SelectionFilter(ISelectionFilter):
    """Filter to select only elements of a specific category."""

    def __init__(self, category_name):
        self.category_name = category_name

    def AllowElement(self, e):
        if e.Category and e.Category.Name == self.category_name:
            return True
        return False

    def AllowReference(self, ref, point):
        return False


def GetCeilingElements():
    """Retrieve Ceiling elements from the active document."""
    refCeilingElements = FilteredElementCollector(doc).OfClass(Ceiling).WhereElementIsNotElementType().ToElements()
    ceilingElements = [doc.GetElement(ref.Id) for ref in refCeilingElements]
    return ceilingElements


def CreateCeilingCurves(ceilingElement):
    """Extract boundary curves from a Ceiling element."""
    curveList = []

    # Get sketch of ceiling
    ceilingSketch = ceilingElement.GetSketch()

    if ceilingSketch:
        # Extract ModelCurves from the sketch
        for modelCurveId in ceilingSketch.GetAllModelCurveIds():
            modelCurve = doc.GetElement(modelCurveId)
            curve = modelCurve.GeometryCurve  # Get the curve geometry
            curveList.append(curve)

    return curveList


"""----------------------MAIN CODE----------------------------"""

try:
    # Get Ceiling elements
    ceilingElements = GetCeilingElements()

    for ceiling in ceilingElements:
        curves = CreateCeilingCurves(ceiling)




# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    TaskDialog.Show("Canceled", "Operation was canceled by the user.")

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
