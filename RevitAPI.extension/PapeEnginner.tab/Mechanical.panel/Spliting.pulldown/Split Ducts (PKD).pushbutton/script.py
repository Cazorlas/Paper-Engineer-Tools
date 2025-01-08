#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr
import math
import System
import sys

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

import Autodesk
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections
from Autodesk.Revit.DB.Mechanical import Duct, MechanicalUtils
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, Separator, Button, CommandLink, TaskDialog, CheckBox
from pyrevit import forms, revit, script
from SubForm import ShowNotification

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

import Revit  # Import Revit namespace in RevitNodes

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

import RevitServices

clr.AddReference("RevitServices")

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

""" ----------------------FUNCTIONS----------------------------"""


class SelectionFilter(ISelectionFilter):
    """Filter to select only elements of a specific category."""

    def __init__(self, category_name):
        self.category_name = category_name

    def AllowElement(self, e):
        if e.Category and e.Category.Name == self.category_name:
            return True
        return False

    def AllowReference(self, ref, point):
        return False


def CollectDuctAuto():
    return FilteredElementCollector(doc, view.Id).OfCategory(
        BuiltInCategory.OST_DuctCurves).WhereElementIsNotElementType().ToElements()


def CollectDuctManual():
    return uidoc.Selection.PickObjects(ObjectType.Element, SelectionFilter('Ducts'), 'Select Ducts')


def GetValidDuct(ducts, desired_length):
    valid_ducts = []

    for duct in ducts:
        family = duct.LookupParameter('Family').AsValueString()
        duct_length_check = duct.LookupParameter('Length').AsDouble()  # ft
        if duct_length_check > desired_length:
            valid_ducts.append(duct)

    return valid_ducts


def ClosestConnectors(el1, el2):
    """Find the closest connectors between two elements."""
    conn1 = el1.ConnectorManager.Connectors
    conn2 = el2.ConnectorManager.Connectors

    dist = float('inf')  # infinity float
    connset = None
    for c in conn1:
        for d in conn2:
            conndist = c.Origin.DistanceTo(d.Origin)
            if conndist < dist:
                dist = conndist
                connset = [c, d]
    return connset


def CheckDir(conn1, conn2):
    """Check if two connectors are aligned in the same or opposite direction."""
    if conn1.CoordinateSystem.BasisZ.ToString() == conn2.CoordinateSystem.BasisZ.ToString() or conn1.CoordinateSystem.BasisZ.ToString() == (
            conn2.CoordinateSystem.BasisZ.Negate()).ToString():
        return True
    else:
        return False


def CreateFittings(ele1, ele2):
    """Create fittings between two elements if possible."""
    fittings = []
    connectors = ClosestConnectors(ele1, ele2)

    with Transaction(doc, 'CreateFittings') as t:
        t.Start()
        try:
            if CheckDir(connectors[0], connectors[1]):
                fitting = doc.Create.NewUnionFitting(connectors[0], connectors[1])
            else:
                fitting = doc.Create.NewElbowFitting(connectors[0], connectors[1])

            fittings.append(fitting)
        except Exception as ex:
            TaskDialog.Show("Error", "Warning: {}".format(ex))

        t.Commit()

    return fittings


def GetDuctunionFamily(duct):
    """Get the Family Union in Routing Preferences of Duct"""
    routing_manager = duct.DuctType.RoutingPreferenceManager
    ruleUnion = routing_manager.GetRule(RoutingPreferenceRuleGroupType.Unions, 0)
    unionType = doc.GetElement(ruleUnion.MEPPartId).Family
    return unionType


def GetConnectorsFromDocument(doc):
    connectors = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_ConnectorElem).WhereElementIsNotElementType().ToElements()
    return connectors


def GetUnionThickness(unionFamily):
    """Get Connectors of Union Family (mm)"""
    UnionfamilyDoc = doc.EditFamily(unionFamily)
    familyConnector = GetConnectorsFromDocument(UnionfamilyDoc)
    connectorPoint1 = familyConnector[0].Origin
    connectorPoint2 = familyConnector[1].Origin
    distanceConnector = connectorPoint1.DistanceTo(connectorPoint2) * 304.8
    # distanceConnector = round(connectorPoint1.DistanceTo(connectorPoint2) * 304.8)
    return distanceConnector


"""----------------------MAIN CODE----------------------------"""
try:
    # refDucts = CollectDuctManual()
    # ductEles = [doc.GetElement(duct.ElementId) for duct in refDucts]
    abc = {'Option 1': 10.0, 'Option 2': 20.0}

    # Khởi tạo các thành phần của Form
    components = [Label('Pick Style:'),
                  Separator(),  # Dấu phân cách làm tiêu đề
                  # ComboBox('combobox1', abc),  # Hộp chọn với các tùy chọn
                  Separator(),  # Dấu phân cách
                  ComboBox('textbox1', abc),  # Hộp chọn thay thế TextBox
                  CheckBox('checkbox1', 'Check this'),  # Ô chọn (Checkbox)
                  Separator(),  # Dấu ngăn cách
                  Button('Select')  # Nút bấm
                  ]

    # Tạo và hiển thị FlexForm
    form = FlexForm('My Custom Form', components)
    result = form.show()

    # Xử lý kết quả từ Form
    if result:
        selected_option = result.get('combobox1')
        entered_text = result.get('textbox1')
        checkbox_state = result.get('checkbox1')




    else:
        pass




except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    # pass
    ShowNotification("Error", "Warning: {}".format(ex))  # Corrected string formatting
