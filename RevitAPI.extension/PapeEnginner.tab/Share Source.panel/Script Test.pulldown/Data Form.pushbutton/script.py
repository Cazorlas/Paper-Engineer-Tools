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

"""----------------------MAIN CODE----------------------------"""

try:
    refEle = selection.PickObjects(ObjectType.Element, "Select Reference Elements")
    eles = [doc.GetElement(ref.ElementId) for ref in refEle]

    nameLst = [e.Name for e in eles]
    idLst = [i.Id.IntegerValue for i in eles]

    f = MainForm(eles)

    # Get the Revit main window handle and assign as owner
    revit_window_handle = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle
    host_window = System.Windows.Forms.Control.FromHandle(revit_window_handle)
    f.Owner = host_window  # Set Revit as the form owner

    # Show the form modelessly
    f.Show()
    # f.TopMost = True  # Keep the form on top of Revit

# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
