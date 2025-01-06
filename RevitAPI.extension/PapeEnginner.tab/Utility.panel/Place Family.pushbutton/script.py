#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv

import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

from rpw.ui.forms import Alert
from rpw.ui.selection import PickObjects

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script
from pyrevit.forms import ProgressBar

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

import Autodesk

from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.DB import Options, GeometryInstance, XYZ
from Autodesk.Revit.DB.Structure import StructuralType

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

""" ----------------------FUNCTIONS----------------------------"""


class SelectionFilter(ISelectionFilter):
    """Filter to select only elements of a specific category."""

    def AllowElement(self, e):
        if isinstance(e, ImportInstance):
            return True
        return False

    def AllowReference(self, ref, point):
        return False


def GetGeometryElement(element):
    """Get geometry of elements"""

    opt = Options()  # Geometrical analysis

    geoByElement = element.get_Geometry(opt)

    return geoByElement


def CADBlocks(cad, geoObj):
    """Get information (points, rotations, blocks, layers) of CAD file"""
    points, rotations, blocks, layersAll = [], [], [], []

    transform = geoObj.Transform
    instance = geoObj.SymbolGeometry
    for inst in instance:
        layers = []
        if isinstance(inst, GeometryInstance):
            origin = transform.OfPoint(inst.Transform.Origin)
            points.append(XYZ(origin.X, origin.Y, origin.Z))  # Convert to Revit XYZ
            # points.append(transform.OfPoint(inst.Transform.Origin).ToPoint()) This is in Dynamo
            rotation = abs(math.degrees(inst.Transform.BasisX.AngleOnPlaneTo(XYZ.BasisX, XYZ.BasisZ)) - 360)
            if round(rotation, 3) == 360:
                rotation = 0
            rotations.append(round(rotation, 3))
            if version > 2022:
                blocks.append(
                    cad.Document.GetElement(inst.GetSymbolGeometryId().SymbolId).ToDSType(True).Name.split(".dwg.")[
                        -1])
            else:
                blocks.append(inst.Symbol.ToDSType(True).Name.split(".dwg.")[-1])
            geom = inst.SymbolGeometry
            for geo in geom:
                try:
                    layers.append(cad.Document.GetElement(geo.GraphicsStyleId).GraphicsStyleCategory.Name)
                except:
                    layers.append(None)
            if layers != []:
                layersAll.append(layers[0])
            else:
                layersAll.append(layers)

    return points, rotations, blocks, layersAll


def GetFamilyByName(familyName):
    """Get Family by Family's Name"""
    allFamily = FilteredElementCollector(doc).OfClass(Family).ToElements()
    for family in allFamily:
        if family.Name == familyName:
            return family

    return None


def GetFamilySymbolByName(family, typeName):
    """Get family by family name and type name"""
    typeIds = family.GetFamilySymbolIds()  # Get all family types of a family
    for typeId in typeIds:
        familySymbol = doc.GetElement(typeId)
        name = familySymbol.LookupParameter("Type Name").AsString()
        if typeName == name:
            return familySymbol

    return None


def PlaceFamilyInstance(points, familySymbol, level):
    """Inserts a new instance of a family into the document, using locations (points), family symbol, level, structuralType"""
    structuralType = StructuralType.NonStructural
    with Transaction(doc, "Place Families") as t:
        t.Start()
        if not familySymbol.IsActive:  # Ensure to active family
            familySymbol.Activate()
        newInstance = doc.Create.NewFamilyInstance(points, familySymbol, level, structuralType)
        t.Commit()
    return newInstance


def tolist(obj):
    """Return items to a list"""
    if hasattr(obj, "__iter__"):
        return obj
    else:
        return [obj]


def IndexOfItem(lstCheck, nameItem):
    """Get index of item in a list"""
    items = tolist(lstCheck)
    lstIndex = []
    for i in tolist(nameItem):
        item1 = i
        indices = []
        for j in range(0, len(items)):
            item2 = items[j]
            if item1 == item2:
                indices.append(j)

        lstIndex.append(indices)

    if len(lstIndex) == 1:
        lstIndex = lstIndex[0]

    return lstIndex


def GetItemAtIndex(lst, index):
    """Get items by index from a list"""
    items = tolist(lst)
    lstItems = []
    for i in index:
        lstItems.append(items[i])

    return lstItems


def GetLevelByName(levelName):
    allLevels = FilteredElementCollector(doc).OfClass(Level).WhereElementIsNotElementType().ToElements()
    for level in allLevels:
        name = level.Name
        if name == levelName:
            return level

    return None


"""----------------------MAIN CODE----------------------------"""
try:
    # Show Guideline for users
    showInfo = TaskDialog.Show('Hello there',
                               'Guideline by PaperEngineer\n\n1. Please select CSV file, remember to format as per template file\n2. Select CAD Link file\n3. Enjoy!!!')

    # Choose csv file and handle
    source_file = forms.pick_file(file_ext='csv')

    """----------------------PROCESS----------------------------"""
    if not source_file:
        Alert('No CSV File Selected. Please Select Again.', exit=True)
    else:
        """----------------------CSV File----------------------------"""
        try:
            with codecs.open(source_file, 'r', encoding='utf-8-sig') as csvfile:
                blockNames, familyNames, typeNames, levelNames, elevations = [], [], [], [], []
                f = csv.reader(csvfile)

                # Skip the header row
                next(f)

                for row in f:
                    blockNames.append(row[0])
                    familyNames.append(row[1])
                    typeNames.append(row[2])
                    levelNames.append(row[3])
                    elevations.append(float(row[4]))

        except Exception as ex:
            TaskDialog.Show("Error", "Warning: {}".format(ex))

        """----------------------CAD FILE----------------------------"""
        points, rotations, blocks, layersAll = [], [], [], []
        try:
            ref = uidoc.Selection.PickObject(ObjectType.Element, SelectionFilter(), 'Select File Link')
            cadFile = doc.GetElement(ref)
            cadTransform = cadFile.GetTransform()

            geoElem = GetGeometryElement(cadFile)

            for geoObj in geoElem:
                pts, rots, blks, lays = CADBlocks(cadFile, geoObj)
                points.extend(pts)
                rotations.extend(rots)
                blocks.extend(blks)
                layersAll.extend(lays)
        except Exception as ex:
            TaskDialog.Show("Error", "Warning: {}".format(ex))

        """----------------------PLACE FAMILY----------------------------"""
        with TransactionGroup(doc, "Place Family as per CAD file") as tg:
            tg.Start()
            for blockName, familyName, typeName, levelName, elevation in zip(blockNames, familyNames, typeNames,
                                                                             levelNames, elevations):
                lstIndex = IndexOfItem(blocks, blockName)
                lstPoints = GetItemAtIndex(points, lstIndex)

                family = GetFamilyByName(familyName)
                familySymbol = GetFamilySymbolByName(family, typeName)

                level = GetLevelByName(levelName)

                if familySymbol and level:
                    for point in lstPoints:
                        adjustedPoint = XYZ(point.X, point.Y, float(elevation) / 304.8)
                        newFamilyInstance = PlaceFamilyInstance(adjustedPoint, familySymbol, level)

                print(50 * "-")
                print("There are {} families to be placed as per CAD Block {}".format(len(lstPoints), blockName))
            tg.Assimilate()


except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    print("Error", "Warning: {}".format(ex))
