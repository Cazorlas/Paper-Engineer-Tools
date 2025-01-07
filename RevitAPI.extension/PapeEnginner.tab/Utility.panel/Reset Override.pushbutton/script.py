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

from SubForm import *

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
selection = uidoc.Selection
version = int(app.VersionNumber)

""" ----------------------FUNCTIONS----------------------------"""


# Hàm Reset Overrides cho các đối tượng được chọn (PascalCase)
def ResetElementOverrides(doc, view, selectedEle):
    overrideSettings = OverrideGraphicSettings()

    with Transaction(doc, "Reset Element Overrides") as t:
        try:
            t.Start()
            for e in selectedEle:
                element = doc.GetElement(e)
                if element:
                    view.SetElementOverrides(element.Id, overrideSettings)

            t.Commit()
            ShowNotification("Success", "Overrides have been reset for selected elements.")
        except Exception as ex:
            t.RollBack()
            ShowNotification("Error", "Failed to reset overrides: {}".format(str(ex)))


""" ---------------------------MAIN------------------------------"""


"""----------------------MAIN CODE----------------------------"""
try:

    # Lấy các đối tượng được chọn
    selectedEle = selection.GetElementIds()

    if selectedEle:
        ResetElementOverrides(doc, view, selectedEle)
    else:
        ShowNotification("No Selection", "Please select elements to reset overrides.")




except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting

