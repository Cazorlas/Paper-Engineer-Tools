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
""" ----------------------FUNCTIONS----------------------------"""


def CollectDuctAuto():
    ductsEles = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_DuctCurves).WhereElementIsNotElementType().ToElements()
    return ductsEles


def GetVerticalDucts(lstDucts):
    verticalDucts = []
    otherDucts = []

    for duct in lstDucts:
        ductCurve = duct.Location.Curve
        lineDirection = ductCurve.Direction
        vectorNormalized = lineDirection.Normalize()
        zAxis = XYZ(0, 0, 1)

        # Tính dot product giữa vector ống và trục Z
        dotProduct = vectorNormalized.DotProduct(zAxis)

        # Nếu dot product gần bằng 1 hoặc -1, đây là ống đứng
        if abs(dotProduct - 1) < 1e-6 or abs(dotProduct + 1) < 1e-6:
            verticalDucts.append(duct)
        else:
            otherDucts.append(duct)

    return verticalDucts, otherDucts


""" ----------------------CODE----------------------------"""
try:
    lstDucts = CollectDuctAuto()
    verticalDucts, otherDucts = GetVerticalDucts(lstDucts)

    if otherDucts:
        selection.SetElementIds(List[ElementId]([e.Id for e in otherDucts]))

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
