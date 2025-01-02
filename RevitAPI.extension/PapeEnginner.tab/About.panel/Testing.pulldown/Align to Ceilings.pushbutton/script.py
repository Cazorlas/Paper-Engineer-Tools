#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library
# from MainForm import MainForm

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

from MainForm import *

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections
from Autodesk.Revit.DB.Mechanical import Duct, MechanicalUtils
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

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


class SelectionFilter(ISelectionFilter):
    """Filter to select only elements of a specific category."""

    def __init__(self, categoryName):
        self.categoryName = categoryName

    def AllowElement(self, e):
        if e.Category and e.Category.Name == self.categoryName:
            return True
        return False

    def AllowReference(self, ref, point):
        return False


def GetCeilings():
    """Get ceiling"""
    refCeiling = uidoc.Selection.PickObjects(ObjectType.Element, SelectionFilter('Ceilings'), 'Select Ceiling')
    ceilings = [doc.GetElement(ref.ElementId) for ref in refCeiling]

    return ceilings


def GetFillPatternsFromCeilings(ceilings):
    """
    Retrieve Fill Patterns from the selected ceilings.
    Parameters:
        ceilings (List[Element]): List of Ceiling elements.
    Returns:
        List[str]: A list of Fill Pattern names from each ceiling.
    """
    fillPatterns = []
    for ceiling in ceilings:
        bottomFaces = HostObjectUtils.GetBottomFaces(ceiling)
        for faceRef in bottomFaces:
            face = ceiling.GetGeometryObjectFromReference(faceRef)
            if face.MaterialElementId != ElementId.InvalidElementId:
                material = doc.GetElement(face.MaterialElementId)
                if material and material.SurfaceForegroundPatternId != ElementId.InvalidElementId:
                    pattern = doc.GetElement(material.SurfaceForegroundPatternId)
                    if pattern:
                        fillPatterns.append(pattern.Name)
                        break
    return fillPatterns

#def

"""----------------------MAIN CODE----------------------------"""
try:

    # Select ceilings from the user
    ceilings = GetCeilings()

    # Extract Fill Patterns from selected ceilings
    fillPatterns = GetFillPatternsFromCeilings(ceilings)

    print(fillPatterns)




except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
