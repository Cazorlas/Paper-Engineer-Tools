#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library
# from MainForm import MainForm

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

from MainForm import *

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections
from Autodesk.Revit.DB.Mechanical import Duct, MechanicalUtils
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

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


# def tolist(obj):
#     """Ensure the object is a list."""
#     if hasattr(obj, "__iter__"):
#         return obj
#     else:
#         return [obj]


def closest_connectors(el1, el2):
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


def check_dir(conn1, conn2):
    """Check if two connectors are aligned in the same or opposite direction."""
    if conn1.CoordinateSystem.BasisZ.ToString() == conn2.CoordinateSystem.BasisZ.ToString() or conn1.CoordinateSystem.BasisZ.ToString() == (
            conn2.CoordinateSystem.BasisZ.Negate()).ToString():
        return True
    else:
        return False


def createFittings(ele1, ele2):
    """Create fittings between two elements if possible."""
    fittings = []
    connectors = closest_connectors(ele1, ele2)

    with Transaction(doc, 'CreateFittings') as t:
        t.Start()
        try:
            if check_dir(connectors[0], connectors[1]):
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
    distanceConnector = round(connectorPoint1.DistanceTo(connectorPoint2) * 304.8)
    return distanceConnector


"""----------------------MAIN CODE----------------------------"""
try:
    """----------------------------RUN FORMS----------------------------"""
    f = MainForm()
    f.ShowDialog()

    # If 'OK' is clicked on the form
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # Get the desired length from the form input
        auto_mode = f._radioButton1.Checked
        manual_mode = f._radioButton2.Checked
        cut_length = float(f._LengthInput.Text)  # mm

        # Check if Auto Mode or Manual Mode is selected
        if auto_mode:
            # Collect all ducts in the active view
            collector_ducts = FilteredElementCollector(doc, view.Id).OfCategory(
                BuiltInCategory.OST_DuctCurves).WhereElementIsNotElementType().ToElements()
            ducts_eles = [doc.GetElement(s.Id) for s in collector_ducts]
        elif manual_mode:
            # Manual duct selection
            collector_ducts = uidoc.Selection.PickObjects(ObjectType.Element, SelectionFilter('Ducts'), 'Select Ducts')
            ducts_eles = [doc.GetElement(s.ElementId) for s in collector_ducts]

        if len(ducts_eles) == 0:
            TaskDialog.Show("Error", "There is no Selected Ducts")
        else:
            # Filter Ducts
            valid_ducts = []
            desired_length = cut_length / 304.8  # ft

            for duct in ducts_eles:
                family = duct.LookupParameter('Family').AsValueString()
                duct_length_check = duct.LookupParameter('Length').AsDouble()  # ft
                if duct_length_check > desired_length:
                    valid_ducts.append(duct)

            # Begin transaction group for splitting ducts
            tg = TransactionGroup(doc, 'Split Ducts')
            tg.Start()
            for duct in valid_ducts:
                duct_cut_id = []  # Reset list
                new_list1_duct = []
                new_list2_duct = []

                # Get the duct length parameter
                duct_length = duct.LookupParameter('Length').AsDouble()  # ft
                duct_union = GetDuctunionFamily(duct)
                duct_thickness = GetUnionThickness(duct_union) / 304.8  # ft

                # Split the duct
                if duct_length > desired_length:
                    # Get the duct curve and start point
                    duct_curve = duct.Location.Curve
                    start_point = duct_curve.GetEndPoint(0)

                    segments_to_create = int(duct_length / (desired_length + (1 / 304.8)))  # How many segments?

                    # Checking------------------------------------------
                    # print("duct_length: {}".format(duct_length*304.8))
                    # print("desired_length: {}".format(desired_length*304.8))
                    # print("segments_to_create: {}".format(segments_to_create))
                    # print("duct_thickness: {}".format(duct_thickness*304.8))

                    # Begin transaction to break the duct
                    t = Transaction(doc, "Split Duct")
                    t.Start()
                    scale = 0
                    for i in range(segments_to_create):
                        if i == 0:
                            scale += desired_length + duct_thickness / 2
                        else:
                            scale += desired_length + duct_thickness

                        cut_point = start_point + (duct_curve.Direction * scale)
                        # vectorDist = duct_curve.Direction.Multiply(scale /304.8)
                        # cut_point = start_point.Add(vectorDist)
                        new_elem_id = MechanicalUtils.BreakCurve(doc, duct.Id, cut_point)  # Split the duct
                        duct_cut_id.append(new_elem_id)

                    duct_cut_id.append(duct.Id)  # Include original duct ID

                    # Create fittings between new duct segments
                    new_list1_duct = [doc.GetElement(e) for e in duct_cut_id]
                    new_list2_duct = new_list1_duct[1:]  # Remove first item of list

                    t.Commit()

                    for ele1, ele2 in zip(new_list1_duct, new_list2_duct):
                        createFittings(ele1, ele2)

            tg.Assimilate()  # Finalize transaction group

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
