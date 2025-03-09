#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr  # Common Language Runtime for .NET
import sys
clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs




from PPGeometry.VisuallizeGeometry import *

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
clr.AddReference("RevitServices")

# Prepare document and other variables
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
unit = doc.GetUnits()
version = int(app.VersionNumber)

# __revit__ = Autodesk.Revit.UI.UIApplication

""" ----------------------FUNCTIONS----------------------------"""

""" ----------------------MAIN CODE----------------------------"""

try:
    point = XYZ(0, 0, 0)
    Visuallize.VisualizePoint(doc,point)










except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
