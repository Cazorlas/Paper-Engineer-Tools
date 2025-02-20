# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python
import sys

from System.Collections.Generic import *  # Lets you handle generics.
from pyrevit import forms, revit, script,EXEC_PARAMS

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

from InputForm import InputForm
import System.Windows.Forms
from System.Windows.Forms import Application

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager  # Tracks the document attached to Dynamo
from RevitServices.Transactions import TransactionManager  # Manages transactions in Dynamo

"""----------------------INPUT----------------------------"""
# Prepare variable and input
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
selection = uidoc.Selection
version = int(app.VersionNumber)
Application.EnableVisualStyles()

"""----------------------FUNCTION----------------------------"""
# TODO: Create functions
def GetParametersInfo(params, version):
    """ Get information parameters of elements"""
    # Initialize lists to store parameter information
    pid, pname, guid, pgroup, ptype, visible, userCreated, builtInParam, utype, dutype, stype, isshared, isreadonly, usermodifiable, hasvalue, value = \
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for param in params:
        defi = param.Definition
        pname.append(defi.Name)
        pid.append(param.Id.IntegerValue)
        try:
            guid.append(param.GUID)
        except:
            guid.append(None)
        pgroup.append(LabelUtils.GetLabelFor(defi.ParameterGroup))

        if version < 2022:
            ptype.append(defi.ParameterType)
            utype.append(defi.UnitType)
            try:
                dutype.append(param.DisplayUnitType)
            except:
                dutype.append(None)
        else:
            ptype.append(
                LabelUtils.GetLabelForSpec(defi.GetDataType()) if SpecUtils.IsSpec(defi.GetDataType()) else "Invalid")
            try:
                utype.append(UnitUtils.GetTypeCatalogStringForSpec(defi.GetDataType()))
            except:
                utype.append(None)
            try:
                dutype.append(UnitUtils.GetTypeCatalogStringForUnit(param.GetUnitTypeId()))
            except:
                dutype.append(None)

        visible.append(defi.Visible)
        isBuiltIn = defi.BuiltInParameter
        userCreated.append(isBuiltIn == BuiltInParameter.INVALID)
        builtInParam.append(isBuiltIn)
        stype.append(param.StorageType)
        isshared.append(param.IsShared)
        isreadonly.append(param.IsReadOnly)
        usermodifiable.append(param.UserModifiable)
        hasvalue.append(param.HasValue)

        if param.StorageType == StorageType.ElementId:
            value.append(
                doc.GetElement(param.AsElementId()) if param.AsElementId().IntegerValue > 0 else param.AsValueString())
        else:
            val = param.AsValueString()
            value.append(val if val is not None else param.AsString())

    return pid, pname, pgroup

def GroupElementsByKeys(items, keys, toSort=True):
    """Functions to group elements by key with optional sorting

    Args:
        items (list): List of items to be grouped
        keys (list): List of keys for grouping
        toSort (bool): If True, sort the unique keys; if False, maintain original order

    Returns:
        tuple: (grouped_lists, unique_keys) where grouped_lists contains grouped items
              and unique_keys is the list of unique keys
    """
    # Create a dictionary for faster grouping
    groupDict = {}

    # Group items by keys using dictionary
    for item, key in zip(items, keys):
        if key not in groupDict:
            groupDict[key] = []
        groupDict[key].append(item)

    # Get unique keys
    uniqueKeys = list(groupDict.keys())

    # Sort keys if toSort is True
    if toSort:
        uniqueKeys.sort()

    # Create grouped lists in the order of unique_keys
    groupedLists = [groupDict[key] for key in uniqueKeys]

    # return groupedLists, uniqueKeys
    return groupDict

def SelectParameters(params, groupKeys, data):
    """Function to select parameters based on user input."""

    f = InputForm(params)
    # Application.Run(f)

    ops = {}

    # Group parameters by their group names
    for i, group in enumerate(groupKeys):
        groupedData = data[i]
        ops[group] = [param.Definition.Name for param in groupedData]

    print(ops)


    # # Group parameters by their group names
    # for i, group in enumerate(groupKeys):
    #     params_in_group = data[i]
    #     ops[group] = [MyOption(param.Definition.Name) for param in params_in_group]
    #
    # # Show selection dialog
    # selectedItems = forms.SelectFromList.show(ops,
    #                                           title='Select Parameters',
    #                                           group_selector_title='Parameter Group:',
    #                                           multiselect=True)
    #
    # selectedParams = []
    # if selectedItems:
    #     for sel in selectedItems:
    #         for param_group, param_names in ops.items():
    #             if sel in {item.name for item in param_names}:
    #                 selectedParams += [
    #                     param for param in params if param.Definition.Name == sel
    #                 ]
    # # return selectedParams


def MatchParameterValue(receive_eles, selected_get_params):
    """ Match parameter values for selected elements """
    with Transaction(doc, "Match Parameter Value") as t:
        t.Start()
        for e in receive_eles:
            for sel_param in selected_get_params:
                try:
                    for rec_param in e.Parameters:
                        if rec_param.Id == sel_param.Id and not rec_param.IsReadOnly:
                            if sel_param.StorageType == StorageType.String:
                                rec_param.Set(sel_param.AsString())
                            elif sel_param.StorageType == StorageType.Integer:
                                rec_param.Set(sel_param.AsInteger())
                            elif sel_param.StorageType == StorageType.Double:
                                rec_param.Set(sel_param.AsDouble())
                            elif sel_param.StorageType == StorageType.ElementId:
                                rec_param.Set(sel_param.AsElementId())
                except Exception as ex:
                    print("Failed to set parameter {}: {}".format(sel_param.Definition.Name, ex))

        t.Commit()

"""----------------------MAIN CODE----------------------------"""
try:
    # TODO: Select element to get parameter and get parameter to transfer
    # Select an element to get parameters
    getRef = uidoc.Selection.PickObject(ObjectType.Element, 'Select element to get')
    getEle = doc.GetElement(getRef.ElementId)

    # Retrieve and organize parameter information
    params = getEle.GetOrderedParameters()
    pId, pName, pGroup = GetParametersInfo(params, version)

    # Sort data into bins
    sortedData = GroupElementsByKeys(pName, pGroup, toSort=False)



    # Select parameters based on user input
    selectedGetParams = SelectParameters(params, sortedData.keys(), sortedData.values())
    if not selectedGetParams:
        sys.exit()
    #
    # # TODO: Select element to receive parameter do Transaction
    # # Select elements to receive parameters
    # receiveRef = uidoc.Selection.PickObjects(ObjectType.Element, 'Select elements to match')
    # receiveEles = [doc.GetElement(ref.ElementId) for ref in receiveRef]
    #
    # # Match parameter values
    # MatchParameterValue(receiveEles, selectedGetParams)

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass
