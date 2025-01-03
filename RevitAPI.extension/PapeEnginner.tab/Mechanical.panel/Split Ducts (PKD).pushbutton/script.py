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

    def __init__(self, category_name):
        self.category_name = category_name

    def AllowElement(self, e):
        if e.Category and e.Category.Name == self.category_name:
            return True
        return False

    def AllowReference(self, ref, point):
        return False


def CollectDuctManual():
    return uidoc.Selection.PickObjects(ObjectType.Element, SelectionFilter('Ducts'), 'Select Ducts')


"""----------------------MAIN CODE----------------------------"""
try:
    refDucts = CollectDuctManual()
    ductEles = [doc.GetElement(duct.ElementId) for duct in refDucts]

    print(ductEles)


except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
