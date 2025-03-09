#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr  # Common Language Runtime for .NET
import System
import sys

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

# sys.path.append("F:\0. Personal\2. Work\2. Python\RevitAPI\Tools\Paper Engineer\RevitAPI.extension\lib\PPGeometry")
# import PPGeometry.VisuallizeGeometry
import VisuallizeGeometry

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
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)

# __revit__ = Autodesk.Revit.UI.UIApplication

""" ----------------------FUNCTIONS----------------------------"""

""" ----------------------MAIN CODE----------------------------"""

try:
    point = XYZ(0, 0, 0)
    Visualize.VisualizePoint(doc,point)










except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
