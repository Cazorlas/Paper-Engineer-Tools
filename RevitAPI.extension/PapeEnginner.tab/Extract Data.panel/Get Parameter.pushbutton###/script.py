# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python

from System.Collections.Generic import *  # Lets you handle generics.
from pyrevit import forms, revit,script

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
# Select an element to get parameters
get_ref = uidoc.Selection.PickObject(ObjectType.Element, 'Select element to get')
get_ele = doc.GetElement(get_ref.ElementId)

# Retrieve all parameters of the selected element
params = get_ele.GetOrderedParameters()

# Initialize lists to store parameter information
pid, pname, guid, pgroup, ptype, visible, userCreated, builtInParam, utype, dutype, stype, isshared, isreadonly, usermodifiable, hasvalue, value = \
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

# Iterate over each parameter
for param in params:
    defi = param.Definition
    pname.append(defi.Name)
    pid.append(param.Id)
    try:
        guid.append(param.GUID)
    except:
        guid.append(None)
    pgroup.append(LabelUtils.GetLabelFor(defi.ParameterGroup))
    if version < 2022:
        ptype.append(defi.ParameterType)
    else:
        if SpecUtils.IsSpec(defi.GetDataType()):
            ptype.append(LabelUtils.GetLabelForSpec(defi.GetDataType()))
        else:
            ptype.append("Invalid")
    visible.append(defi.Visible)
    isBuiltIn = defi.BuiltInParameter
    userCreated.append(isBuiltIn == BuiltInParameter.INVALID)
    builtInParam.append(isBuiltIn)
    if version < 2022:
        utype.append(defi.UnitType)
        try:
            dutype.append(param.DisplayUnitType)
        except:
            dutype.append(None)
    else:
        try:
            utype.append(UnitUtils.GetTypeCatalogStringForSpec(defi.GetDataType()))
        except:
            utype.append(None)
        try:
            dutype.append(UnitUtils.GetTypeCatalogStringForUnit(param.GetUnitTypeId()))
        except:
            dutype.append(None)
    stype.append(param.StorageType)
    isshared.append(param.IsShared)
    hasvalue.append(param.HasValue)
    if param.StorageType == StorageType.ElementId:
        if param.AsElementId().IntegerValue > 0:
            value.append(doc.GetElement(param.AsElementId()))
        else:
            value.append(param.AsValueString())
    else:
        val = param.AsValueString()
        if val is None:
            value.append(param.AsString())
        else:
            value.append(val)
    isreadonly.append(param.IsReadOnly)
    usermodifiable.append(param.UserModifiable)

##################################
# Get input
data = pname  # Data (list of same length as criteria) to be binned
criteria = pgroup  # List of criteria related to the data
toSort = False  # Whether to sort keys

# Find a unique set of values for the criteria, a list of all the bins
# to sort data into
bins = []
sorted = []

for i in range(1, len(criteria)):
    if criteria[i] in bins:
        continue
    else:
        bins.append(criteria[i])
        sorted.append([])  # initialize an empty list

# Sort bins if requested
if toSort:
    bins.sort()

# Sort data into bins
for i in range(len(criteria)):
    for j in range(len(bins)):
        if criteria[i] == bins[j]:
            temp = sorted[j]
            temp.append(data[i])
            sorted[j] = temp
            continue

##########################################
# ops = {'Sheet Set A': ["viewsheet1", "viewsheet2", "viewsheet3"],
#        'Sheet Set B': ["viewsheet4", "viewsheet5", "viewsheet6"]}


ops = dict(zip(bins, sorted))
ops.update({"All": pname})

res = forms.SelectFromList.show(ops,
                                title='MultiGroup List',
                                group_selector_title='Select Integer Range:',
                                multiselect=True
                                )



# Map selected items back to Revit parameters
selected_params = []

# Iterate over the selected items in res
if res:
    for selected_item in res:
        # Match with the original parameters
        for param in params:
            if param.Definition.Name == selected_item:
                selected_params.append(param)
                break

# Now 'selected_params' contains the Revit API parameter objects corresponding to the user's selection
for sel_param in selected_params:
    print(sel_param)
    print(sel_param.Definition.Name)
    print(sel_param.Id)



###########################################
# Output the parameter names (or any other required information)


# receive_ref = uidoc.Selection.PickObjects(ObjectType.Element, 'Select elements to match')
# receive_ele = [doc.GetElement(ref.ElementId) for ref in receive_ref]
