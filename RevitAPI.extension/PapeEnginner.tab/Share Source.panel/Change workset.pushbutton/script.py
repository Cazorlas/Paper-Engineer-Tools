# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python

from System.Collections.Generic import *  # Lets you handle generics.
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # A Dynamo library for its proxy geometry class
from Autodesk.DesignScript.Geometry import *  # Loads everything in Dynamo's

clr.AddReference("RevitAPI")  # Adding reference to Revit's API DLLs
clr.AddReference("RevitAPIUI")  # Adding reference to Revit's API DLLs

import Autodesk  # Loads the Autodesk namespace
from Autodesk.Revit.DB import *  # Loading Revit's API classes
from Autodesk.Revit.UI import *  # Loading Revit's API UI classes
from Autodesk.Revit.UI.Selection import ObjectType  # Import ObjectType to handle selection

clr.AddReference("RevitNodes")  # Dynamo's nodes for Revit
import Revit  # Loads in the Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import \
    DocumentManager  # An internal Dynamo class that keeps track of the document that Dynamo is currently attached to
from RevitServices.Transactions import \
    TransactionManager  # A Dynamo class for opening and closing transactions to change the Revit document's database

# TODO: Prepare variable and input
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)

# ----------------------Main Code----------------------------
try:
    # Select an element to get parameters
    get_ref = uidoc.Selection.PickObject(ObjectType.Element, 'Select element to get')
    get_ele = doc.GetElement(get_ref.ElementId)

    # Get the workset parameter from the selected element
    workset_param = get_ele.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)

    # Get the workset name and ID
    workset_name = workset_param.AsValueString()
    workset_id = WorksetId(workset_param.AsInteger())

    # Start a transaction to modify the active workset
    with Transaction(doc, 'Set Active Workset') as t:
        t.Start()

        # Get the workset table
        workset_table = doc.GetWorksetTable()

        # Set the active workset using the WorksetId
        workset_table.SetActiveWorksetId(workset_id)

        # Commit the transaction
        t.Commit()

    # Notify the user of success
    TaskDialog.Show("Success", "Active workset is: {}".format(workset_name))

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass
