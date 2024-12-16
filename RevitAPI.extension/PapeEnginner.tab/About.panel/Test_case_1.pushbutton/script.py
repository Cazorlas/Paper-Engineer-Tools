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

uiviews = uidoc.GetOpenUIViews()
uiview = [x for x in uiviews if x.ViewId == view.Id][0]

# ------Note: __revit__ = Autodesk.Revit.UI.UIApplication
"""----------------------FUNCTION----------------------------"""

"""----------------------MAIN CODE----------------------------"""

try:
    refEle = uidoc.Selection.PickObjects(ObjectType.Element, "Change Workset")
    ele = [doc.GetElement(ref.ElementId) for ref in refEle]

    worksetCollector = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()

    if worksetCollector is None:
        TaskDialog.Show("Warning", "Not a working share file")
    else:
        worksetName = [i.Name for i in worksetCollector]
        worksetId = [i.Id.IntegerValue for i in worksetCollector]

        dictWorkset = dict(zip(worksetName, worksetId))

        selectedWorksetName = forms.ask_for_one_item(
            worksetName,
            default=worksetName[0],
            prompt='Choose Workset',
            title='Select Workset')

        worksetIdChoose = dictWorkset.get(selectedWorksetName)

        with TransactionGroup(doc, "Set Workset") as tg:
            tg.Start()
            for e in ele:
                worksetPara = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
                worksetPara.Set(worksetIdChoose)
                tg.Assimilate()
            tg.RollBack()
            TaskDialog.Show("Success","Done")














# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass


# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
