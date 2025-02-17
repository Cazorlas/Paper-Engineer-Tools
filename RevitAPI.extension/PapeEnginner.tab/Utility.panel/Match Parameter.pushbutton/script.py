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

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager  # Tracks the document attached to Dynamo
from RevitServices.Transactions import TransactionManager  # Manages transactions in Dynamo


# ----------------------FUNCTION----------------------------
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


def BinData(data, criteria, toSort=True):
    """Functions to group element by key"""
    bins = []
    sorted_data = []

    for i in range(1, len(criteria)):
        if criteria[i] not in bins:
            bins.append(criteria[i])
            sorted_data.append([])

    if toSort:
        bins.sort()

    for i in range(len(criteria)):
        for j in range(len(bins)):
            if criteria[i] == bins[j]:
                sorted_data[j].append(data[i])

    return dict(zip(bins, sorted_data))

# Định nghĩa lớp MyOption để tạo danh sách checkbox với tên tùy chọn
class MyOption(forms.TemplateListItem):
    def __init__(self, orig_item, checked=False):
        """
        Gói một đối tượng (tên danh mục) vào danh sách checkbox.

        Args:
            orig_item (str): Tên danh mục
            checked (bool): Trạng thái ban đầu của checkbox (mặc định là False)

        """
        super(MyOption, self).__init__(orig_item, checked=checked)
        self.item = orig_item  # Lưu trữ danh mục ban đầu

    @property
    def name(self):
        return "{}".format(self.item)  # Hiển thị tên danh mục trong danh sách


def SelectParameters(params, bins, sorted_data):
    """Function to select parameters based on user input"""
    ops = {}
    config = script.get_config(EXEC_PARAMS.command_name)
    previousSelectedItems = config.get_option('selected_items', [])

    # Group parameters by their group names
    for i in range(len(bins)):
        group = bins[i]
        params_in_group = sorted_data[i]  # Get the list of parameters for the current group
        ops[group] = params_in_group  # Map the group to its parameters

    # Add 'All' group
    all_params = [param.Definition.Name for param in params]
    # ops['All'] = all_params
    ops['All'] = [MyOption(param, checked= param in previousSelectedItems) for param in all_params]

    res = forms.SelectFromList.show(ops,
                                    title='MultiGroup List',
                                    group_selector_title='Select Parameter Group:',
                                    multiselect=True)
    config.selected_items = res if res else []
    script.save_config()

    selectedParams = []

    if res:
        for selected_item in res:
            if selected_item == 'All':
                # If 'All' is selected, add all parameters
                selectedParams = params
            else:
                # Otherwise, handle specific groups
                for param_group, param_names in ops.items():
                    if selected_item in param_names:
                        for param in params:
                            param_group_name = LabelUtils.GetLabelFor(param.Definition.ParameterGroup)
                            # Match both name and group
                            if param.Definition.Name == selected_item and param_group_name == param_group:
                                selectedParams.append(param)
                                break

    return selectedParams

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


# ----------------------INPUT----------------------------
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

# ----------------------MAIN CODE----------------------------
"""
with TransactionGroup(doc, 'Match Parameters') as tg:
    tg.Start()
    try:
        while True:
            # TODO: Select element to get parameter and get parameter to transfer
            # Select an element to get parameters
            get_ref = uidoc.Selection.PickObject(ObjectType.Element, 'Select element to get')
            get_ele = doc.GetElement(get_ref.ElementId)

            # Retrieve and organize parameter information
            get_params = get_ele.GetOrderedParameters()
            pid, pname, pgroup = get_parameters_info(get_params, version)

            # Sort data into bins
            sorted_data = bin_data(pname, pgroup, toSort=False)

            # Select parameters based on user input
            selected_get_params = select_parameters(get_params, sorted_data.keys(), sorted_data.values())

            # TODO: Select element to receive parameter do Transaction
            # Select elements to receive parameters
            receive_ref = uidoc.Selection.PickObjects(ObjectType.Element, 'Select elements to match')
            receive_eles = [doc.GetElement(ref.ElementId) for ref in receive_ref]

            # Match parameter values
            match_parameter_value(receive_eles, selected_get_params)

    except Autodesk.Revit.Exceptions.OperationCanceledException:
        pass
    tg.Assimilate()
"""

try:
    # TODO: Select element to get parameter and get parameter to transfer
    # Select an element to get parameters
    getRef = uidoc.Selection.PickObject(ObjectType.Element, 'Select element to get')
    getEle = doc.GetElement(getRef.ElementId)

    # Retrieve and organize parameter information
    getParams = getEle.GetOrderedParameters()
    pId, pName, pGroup = GetParametersInfo(getParams, version)

    # Sort data into bins
    sortedData = BinData(pName, pGroup, toSort=False)

    # Select parameters based on user input
    selectedGetParams = SelectParameters(getParams, sortedData.keys(), sortedData.values())
    if not selectedGetParams:
        sys.exit()

    # TODO: Select element to receive parameter do Transaction
    # Select elements to receive parameters
    receiveRef = uidoc.Selection.PickObjects(ObjectType.Element, 'Select elements to match')
    receiveEles = [doc.GetElement(ref.ElementId) for ref in receiveRef]

    # Match parameter values
    MatchParameterValue(receiveEles, selectedGetParams)

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass
