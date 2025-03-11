#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr  # Common Language Runtime for .NET

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
import Revit  # Import Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

from PPSelection.SelectionFilter import *
from PPGeometry.VisuallizeGeometry import *

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


def PlaneDuct(eleDuct, axis=XYZ.BasisZ):
    curveDuct = eleDuct.Location.Curve
    pointDuct = curveDuct.GetEndPoint(0)

    planeDuct = Plane.CreateByNormalAndOrigin(axis, pointDuct)

    return pointDuct,planeDuct


def GetPointOfFamilyInstance(family):
    points = []

    try:
        connectors = family.MEPModel.ConnectorManager.Connectors
    except:
        try:
            connectors = family.ConnectorManager.Connectors
        except:
            points.append(None)
        return points

    for conn in connectors:
        points.append(conn.Origin)

    return points

def PlaneAirTerminals(pointAT, axis=XYZ.BasisZ):
    return Plane.CreateByNormalAndOrigin(axis, pointAT)

def GetDistanceFromTwoVectors(fromPoint,ToPoint,vectorToMesure = XYZ.BasisZ):
    vectorBtw = ToPoint - fromPoint
    distance = vectorBtw.DotProduct(vectorToMesure)

    return distance



# def ChangeParaCollor(eleAt, distance):
#     collorLength = eleAt.LookupParameter("Collar_Length")
#
#     if collorLength is None:
#         raise ValueError("Parameter 'Collar_Length' not found in element.")
#
#
#     currentValue = collorLength.AsDouble()  # Lấy giá trị hiện tại
#     newValue = currentValue + distance  # Cộng thêm khoảng cách
#
#     with Transaction(doc, "Adjust Collar Length") as t:
#         t.Start()
#         collorLength.Set(newValue)
#         t.Commit()

def ChangeParaCollor(eleAt, distance):
    collorLength = eleAt.LookupParameter("Collar_Length")

    if collorLength is None:
        raise ValueError("Parameter 'Collar_Length' not found in element.")

    # Chuyển từ Feet → Millimeters
    distance = UnitUtils.ConvertFromInternalUnits(distance, UnitTypeId.Millimeters)

    currentValue = UnitUtils.ConvertFromInternalUnits(collorLength.AsDouble(), UnitTypeId.Millimeters)
    newValue = currentValue + distance  # Cộng thêm khoảng cách

    # Chuyển ngược lại sang đơn vị Feet để đặt vào Revit
    newValue_feet = UnitUtils.ConvertToInternalUnits(newValue, UnitTypeId.Millimeters)

    with Transaction(doc, "Adjust Collar Length") as t:
        t.Start()
        collorLength.Set(newValue_feet)  # Set giá trị đã chuyển về Feet
        t.Commit()

""" ----------------------MAIN CODE----------------------------"""

try:
    # print(unit)

    with forms.WarningBar(title='Select Reference Duct'):
        lstFilter = ["Ducts"]
        selectedEle = uidoc.Selection.PickObject(ObjectType.Element,FilterSelection(lstFilter))
        eleDuct = doc.GetElement(selectedEle.ElementId)

    pointDuct, planeDuct = PlaneDuct(eleDuct)
    # Visualize.VisualizePlane(doc,planeDuct)

    while True:
        with forms.WarningBar(title='Select Reference Air Terminals'):
            lstFilter = ["Air Terminals"]
            selectedEle = uidoc.Selection.PickObject(ObjectType.Element, FilterSelection(lstFilter))
            eleAt = doc.GetElement(selectedEle.ElementId)

        lstPoint = GetPointOfFamilyInstance(eleAt)
        pointAT = lstPoint[0]
        planeAT = PlaneAirTerminals(pointAT)

        # Visualize.VisualizePlane(doc,planeAT)
        distance = GetDistanceFromTwoVectors(pointAT,pointDuct)
        with TransactionGroup(doc,"Adjust Collor Length") as tg:
            tg.Start()
            ChangeParaCollor(eleAt,distance)
            tg.Assimilate()






except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
