#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clr
import math
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
import sys
from pyrevit import forms

# Import Minh Tran library
from ElementGeometry import *
from ModelSelection import *
from VisuallizeGeometry import *
from RevitUtils import *


doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB


#---------------------------Function--------------------------------------------


class FittingSelectionFilter(ISelectionFilter):
    def AllowElement(self, element):
        if "Fitting" in element.Category.BuiltInCategory.ToString():
            return True
        return False

    def AllowReference(self, reference, position):

        return False




#---------------------------Main Logic------------------------------------------
filter = FittingSelectionFilter()
sourceEle =  ModelSelection.PickElementsByFilter(uidoc,filter)

# Inpur form
angle = forms.ask_for_string(
    default='90',
    prompt='Enter the Angle (degree)',
    title='Angle'
)

for e in sourceEle:
    sourceConnectors = RevitUtils.GetElementConnectors(e)
    if all(connector.IsConnected for connector in sourceConnectors):
        sys.exit()

    sourceConnector = None
    for connector1 in sourceConnectors:
        if connector1.IsConnected:
            sourceConnector = connector1
            break

    sourceDirection = sourceConnector.CoordinateSystem.BasisZ
    sourceEndPoint = sourceConnector.Origin


    try :
        angle = float(angle)
    except:
        TaskDialog.Show("Error","Please enter a number.")

    # Create rotation transform to rotate target element
    rotationTransform = Transform.CreateRotationAtPoint(sourceDirection, angle, sourceEndPoint)

    #---------------------------Execution-------------------------------------------
    with TransactionGroup(doc, "Rotate Fitting") as tg:
        tg.Start()
        location = e.Location
        center = location.Point
        with Transaction(doc,"Transform element") as t:
            t.Start()
            try:
                # Rotate element
                offsetCenter = center + 0.5*sourceDirection
                axis = Line.CreateBound(center, offsetCenter)
                ElementTransformUtils.RotateElement(doc, e.Id, axis, math.radians(angle))

                # Translate element
                transformedPoint = rotationTransform.OfPoint(center)
                location.Point = transformedPoint

            except Exception as er:
                print (er)
            t.Commit()

        tg.Assimilate()