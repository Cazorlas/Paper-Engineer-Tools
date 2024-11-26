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

# ------Note: __revit__ = Autodesk.Revit.UI.UIApplication

"""----------------------MAIN CODE----------------------------"""

try:
    # Ask the user to select linked elements in the Revit model
    eleRef = selection.PickObjects(ObjectType.LinkedElement, "Select Elements to check IDs")

    eleLst = []  # Initialize an empty list to store the linked elements

    for e in eleRef:
        ele = doc.GetElement(e)  # Get the selected element in the main document

        # Check if the selected element is a RevitLinkInstance
        if isinstance(ele, RevitLinkInstance):
            docLink = ele.GetLinkDocument()  # Get the linked document
            if docLink:  # Ensure the linked document is valid
                eleLink = docLink.GetElement(e.LinkedElementId)  # Get the element from the linked document
                eleLst.append(eleLink)  # Append the linked element to the list

    # Extract the names and IDs of the linked elements
    nameLst = [e.Name for e in eleLst if eleLst]  # Get the names of the linked elements
    idLst = [i.Id.IntegerValue for i in eleLst if eleLst]  # Get the integer IDs of the linked elements

    # Print the results to the console
    print("Selected Linked Element Names:")
    print(nameLst)
    print(50 * "-")  # Print a separator line
    print("Selected Linked Element IDs:")
    print(idLst)

# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
