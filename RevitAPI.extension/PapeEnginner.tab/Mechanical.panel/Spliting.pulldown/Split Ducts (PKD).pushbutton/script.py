#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr
import math
import System

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from ElementGeometry import *
from ModelSelection import *
from VisualizeGeometry import *
from RevitUtils import *

import Autodesk
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.DB.Mechanical import Duct, MechanicalUtils
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, Separator, Button, CommandLink, CheckBox
from pyrevit import forms, revit, script
# from SubForm import ShowNotification
from MainForm import MainForm

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

import Revit  # Import Revit namespace in RevitNodes

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
clr.AddReference("RevitServices")

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

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


def CollectDuctAuto():
    ductsEles = FilteredElementCollector(doc, view.Id).OfClass(Duct).WhereElementIsNotElementType().ToElements()
    return ductsEles


def CollectDuctManual():
    collectorDucts = uidoc.Selection.PickObjects(ObjectType.Element, SelectionFilter('Ducts'), 'Select Ducts')
    ductsEles = [doc.GetElement(s.ElementId) for s in collectorDucts]
    return ductsEles


def flattenLv4(lst):
    return [z for sub_lst in lst for nest_lst in sub_lst for z in nest_lst]


def flattenLv3(lst):
    return [i for sub_lst in lst for i in sub_lst]


def flattenLv2(lst):
    return [i for i in lst]


def GetValidDucts(ducts, stepLength):
    """
    Filters and returns ducts that have a length greater than the specified step length.

    :param ducts (list): A list of duct elements to be filtered.
    :param stepLength (float): The minimum length threshold in feet.

    :return list: A list of ducts with lengths greater than the specified step length.
    """
    validDucts = []

    for duct in ducts:
        # Retrieve the 'Length' parameter of the duct (in feet)
        ductLength = duct.LookupParameter('Length').AsDouble()  # ft

        # Check if the duct length exceeds the specified threshold
        if ductLength > stepLength:
            validDucts.append(duct)

    return validDucts


def CollectLinkData():
    """
    Collect all required data about Revit links in the model.
    """
    refLinkInstance = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    linkType = [doc.GetElement(ref.GetTypeId()) for ref in refLinkInstance]
    linkedTransform = [linkedInstance.GetTransform() for linkedInstance in refLinkInstance]
    docLink = [ref.GetLinkDocument() for ref in refLinkInstance]

    nameLink = [link.LookupParameter("Type Name").AsString() for link in linkType] if linkType else [
        "No Link"]

    statusLoad = ["Loaded" if i is not None else "Not Loaded" for i in docLink]

    filteredLinkNames = ["No Link"] + [nameLink[i] for i, status in enumerate(statusLoad) if status == "Loaded"]
    filteredLinkInstances = [refLinkInstance[i] for i, status in enumerate(statusLoad) if status == "Loaded"]

    return filteredLinkNames, filteredLinkInstances, linkedTransform


def GetWalls(refLinkInstance):
    """
    Thu thập danh sách tường từ mô hình hiện tại hoặc liên kết.
    :param refLinkInstance: Danh sách liên kết RevitLinkInstance hoặc None.
    :return: Danh sách các tường (walls).
    """
    walls = []

    if refLinkInstance is None:
        # Thu thập tường từ tài liệu hiện tại
        refwalls = FilteredElementCollector(doc, view.Id).OfCategory(
            BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
        walls = [doc.GetElement(wall.Id) for wall in refwalls]

    else:

        # Kiểm tra tài liệu liên kết
        linkedDoc = refLinkInstance.GetLinkDocument()

        # Thu thập tường từ tài liệu liên kết
        refwalls = FilteredElementCollector(linkedDoc, view.Id).OfCategory(
            BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
        # walls = [linkedDoc.GetElement(wall.LinkedElementId) for wall in refwalls]
        walls = refwalls

    return walls


def GetElementSolids(element):
    solids = []
    options = Options()
    options.ComputeReferences = True
    geometryElement = element.get_Geometry(options)
    if geometryElement:
        for geometryObject in geometryElement:
            if isinstance(geometryObject, Solid) and geometryObject.Volume > 0:
                solids.append(geometryObject)
            elif isinstance(geometryObject, GeometryInstance):
                for instanceGeometryObject in geometryObject.GetInstanceGeometry():
                    if isinstance(instanceGeometryObject, Solid) and instanceGeometryObject.Volume > 0:
                        solids.append(instanceGeometryObject)
    return solids


def GetMidPointOfLine(line):
    """
    Lấy điểm giữa (midpoint) của một đường thẳng (line).
    :param line: Đối tượng đường thẳng (Line).
    :return: Điểm giữa (XYZ).
    """
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    return XYZ((start.X + end.X) / 2, (start.Y + end.Y) / 2, (start.Z + end.Z) / 2)


def GetWallSolids(wall):
    """
    Lấy đối tượng hình học (solid) từ tường.
    :param wall: Đối tượng tường.
    :return: Danh sách các đối tượng Solid của tường.
    """
    solids = []
    options = Options()
    geometry = wall.get_Geometry(options)
    for geo in geometry:
        if isinstance(geo, Solid) and geo.Volume > 0:
            solids.append(geo)
    return solids


def GetIntersectingElements(linkInstance, walls, ducts):
    intersectingData = []

    opt = Options()
    opt.ComputeReferences = True
    intersectOptions = SolidCurveIntersectionOptions()

    if linkInstance is None:
        transform = Transform.Identity
    else:
        transform = linkInstance.GetTransform()

    for duct in ducts:
        ductCurve = duct.Location.Curve
        wallsForDuct = []  # Danh sách walls giao cắt với duct
        midpointsForDuct = []  # Danh sách midpoints của duct
        linesForDuct = []

        for wall in walls:
            wallSolids = wall.Geometry[opt]

            for wallSolid in wallSolids:
                transformedWallSolid = SolidUtils.CreateTransformed(wallSolid, transform)
                intersection = transformedWallSolid.IntersectWithCurve(ductCurve, intersectOptions)
                if intersection.SegmentCount > 0:
                    # Lấy điểm giữa của giao điểm
                    line = intersection.GetCurveSegment(0)
                    midpoint = GetMidPointOfLine(line)

                    # Thêm wall và midpoint vào danh sách
                    wallsForDuct.append(wall)
                    midpointsForDuct.append(midpoint)
                    linesForDuct.append(line)

        # Thêm thông tin duct vào kết quả
        intersectingData.append({
            "Duct": duct,
            "Walls": wallsForDuct,
            "Midpoints": midpointsForDuct,
            "Lines": linesForDuct
        })

    return intersectingData


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


def SplitDuct(doc, duct, desiredLength, ductThickness):
    """
    Splits a duct into multiple segments based on the desired length.

    Parameters:
        doc (Document): The Revit document.
        duct (Element): The duct to be split.
        desiredLength (float): The desired length for each duct segment (in feet).
        ductThickness (float): The union thickness to account for when splitting (in feet).

    Returns:
        list: A list of Element IDs for the newly created duct segments, including the original duct ID.
    """
    # Lấy độ dài và đường cong của ống
    ductLength = duct.LookupParameter('Length').AsDouble()  # ft
    ductCurve = duct.Location.Curve
    startPoint = ductCurve.GetEndPoint(0)

    # Xác định số đoạn cần tạo
    segmentsToCreate = int(ductLength / (desiredLength + ductThickness))

    # Danh sách để lưu các đoạn ống mới
    newElemIds = []

    # Bắt đầu transaction để cắt ống
    t = Transaction(doc, "Split Duct")
    t.Start()
    scale = 0
    for i in range(segmentsToCreate):
        # Tính điểm cắt
        if i == 0:
            scale += desiredLength + (ductThickness / 2)
        else:
            scale += desiredLength + ductThickness

        cutPoint = startPoint + (ductCurve.Direction * scale)

        # Cắt ống tại điểm cắt
        newElemId = MechanicalUtils.BreakCurve(doc, duct.Id, cutPoint)
        newElemIds.append(newElemId)

    # Thêm ID của ống gốc vào danh sách
    newElemIds.append(duct.Id)

    t.Commit()

    return newElemIds


def GetOffSetPoints(offsets, vectors, points):
    """
    Computes offset points based on the given points and their respective direction vectors.

    :param offsets: The offset distance.
    :param vectors: A list of lists of direction vectors (XYZ).
    :param points: A list of lists of origin points (XYZ).
    :return: A nested list of offset points with positive and negative offsets.
    """
    # Validate input lengths
    if len(points) != len(vectors):
        raise ValueError("The number of sublists in points and vectors does not match!")

    result = []  # List to store the offset points

    for i, sublistPoints in enumerate(points):
        directionSublist = vectors[i]  # Get the corresponding sublist of vectors
        tempResult = []  # Temporary list for storing offset results

        if len(sublistPoints) != len(directionSublist):
            raise ValueError("The number of points and vectors in each sublist does not match!")

        for j, point in enumerate(sublistPoints):
            direction = directionSublist[j].Normalize()  # Normalize the vector
            # Compute positive and negative offset points
            positiveOffset = point + (direction * offsets)  # Positive offset
            negativeOffset = point - (direction * offsets)  # Negative offset
            tempResult.append([positiveOffset, negativeOffset])  # Add the pair to the sublist

        result.append(tempResult)  # Add the sublist to the result

    return result

def ProcessList(lstpoints):
    """
    Chuyển đổi groupedOffsetPoints thành danh sách như mong muốn.

    :param lstpoints: Danh sách lồng nhau của groupedOffsetPoints.
    :return: Danh sách được tái cấu trúc.
    """
    restructured = []
    for sublist in lstpoints:
        # Làm phẳng từng sublist ở cấp độ 2
        flattenedSublist = [point for pair in sublist for point in pair]
        restructured.append(flattenedSublist)
    return restructured

def GroupOffsetPoints(offsetPoints, intersectingPoints):
    """
    Groups offset points by ducts, where each duct has subgroups of offset points for each intersection.

    :param offsetPoints: Nested list of offset points (organized by ducts and intersections).
    :param intersectingPoints: Original nested list of intersecting points (organized by ducts).
    :return: List of grouped offset points by duct, with each duct containing subgroups of offset points.
    """
    groupedPoints = []  # List to store grouped offset points by duct

    # Check that offsetPoints and intersectingPoints have the same outer structure
    if len(offsetPoints) != len(intersectingPoints):
        raise ValueError("Mismatch between offsetPoints and intersectingPoints structure!")

    # Loop through each duct in intersectingPoints
    for ductOffsets, ductIntersections in zip(offsetPoints, intersectingPoints):
        if len(ductOffsets) != len(ductIntersections):
            raise ValueError("Mismatch between offset points and intersecting points for a duct!")

        ductGroup = []  # List to store offset points for the current duct
        for offsets in ductOffsets:
            # Each offsets corresponds to a pair of points [positiveOffset, negativeOffset]
            ductGroup.append(offsets)
        groupedPoints.append(ductGroup)

    return ProcessList(groupedPoints)


def SortPointByLineDirectionNested(lines, lstPoints):
    """
    Xử lý danh sách cấp 2 của line và point.
    lines: Danh sách các đường thẳng (nested list).
    lstPoints: Danh sách các danh sách điểm (nested list).

    Trả về:
    sortedPointsList: Danh sách các điểm đã được sắp xếp theo hướng của đường thẳng tương ứng.
    """
    sortedPointsList = []
    for line, points in zip(lines, lstPoints):
        # Đảm bảo cả line và points không rỗng
        if line and points:
            direction = line.Direction.Normalize()  # Lấy vector chỉ phương của line
            sortedPoints = sorted(points, key=lambda point: direction.DotProduct(point))  # Sắp xếp theo DotProduct
            sortedPointsList.append(sortedPoints)
        else:
            # Nếu line hoặc points rỗng, thêm giá trị rỗng vào danh sách kết quả
            sortedPointsList.append([])
    return sortedPointsList



"""----------------------MAIN CODE----------------------------"""
try:
    nameLink, refLinkInstance, linkedTransform = CollectLinkData()
    nameLinkRemoveFirst = nameLink[1:]
    dictionary = dict(zip(nameLinkRemoveFirst, refLinkInstance))

    """----------------------------RUN FORMS----------------------------"""

    f = MainForm(nameLink)
    f.ShowDialog()

    # If 'OK' is clicked on the form
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # Get the desired length from the form input
        autoMode = f._radioButtonAuto.Checked
        manualMode = f._radioButtonManual.Checked
        stepLength = float(f._textBoxStep.Text)  # mm
        cutLength = stepLength / 304.8  # ft
        stepWall = float(f._textBoxWall.Text)
        linkName = f._comboBoxLink.Text

        if linkName == "No Link":
            chooseRefLink = None

        else:
            chooseRefLink = dictionary.get(linkName)

        # Gọi hàm GetWalls để lấy danh sách tường
        walls = GetWalls(chooseRefLink)

        # print(walls)

        # Check if Auto Mode or Manual Mode is selected
        if autoMode:
            # Collect all ducts in the active view
            ducts = CollectDuctAuto()

        elif manualMode:
            # Manual duct selection
            ducts = CollectDuctManual()

        if len(ducts) == 0:
            TaskDialog.Show("Error", "There is no Selected Ducts")
            exit()

        # Check intersections between walls and ducts
        intersectingData = GetIntersectingElements(chooseRefLink, walls, ducts)

        intersectingDucts = []
        intersectingWalls = []
        intersectingPoints = []
        intersectingLines = []

        notIntersectingDucts = []

        # Hiển thị kết quả
        for data in intersectingData:
            duct = data["Duct"]
            walls = data["Walls"]
            midpoints = data["Midpoints"]
            lines = data["Lines"]

            if walls:
                # print("Duct: {}".format(duct.Id))
                # print("Intersecting Walls: {}".format([wall.Id for wall in walls]))
                # print("Midpoints: {}".format(midpoints))
                intersectingDucts.append(duct)
                intersectingWalls.append(walls)
                intersectingPoints.append(midpoints)
                intersectingLines.append(lines)
            else:
                notIntersectingDucts.append(duct)
                # print("Duct: {}".format(duct.Id))
                # print("Intersecting Walls: []")
                # print("Midpoints: []")

        # print(intersectingPoints)

        lstVector = [l.Direction for lines in intersectingLines for l in lines]
        firstLine = [line[0] for line in intersectingLines]
        # print(intersectingDucts)
        # print(50*"-")
        # print(intersectingLines)
        # print(50*"-")
        # print(lstVector)
        # print(50*"-")
        # print(intersectingPoints)

        # Align lstVector with intersectingPoints
        alignedVectors = []
        vectorIndex = 0
        for pointSublist in intersectingPoints:
            sublistVectors = []
            for _ in pointSublist:
                sublistVectors.append(lstVector[vectorIndex])
                vectorIndex += 1
            alignedVectors.append(sublistVectors)

        # print(alignedVectors)

        offSet = 500 / 304.8
        offsetPoints = GetOffSetPoints(offSet, alignedVectors, intersectingPoints)
        # print(offsetPoints)
        # print(50 * "-")
        # print(intersectingPoints)
        # print(50 * "-")
        groupedOffsetPoints = GroupOffsetPoints(offsetPoints, intersectingPoints)
        # print(groupedOffsetPoints)
        # print(50 * "-")
        sortPoints = SortPointByLineDirectionNested(firstLine, groupedOffsetPoints)
        # print(sortPoints)
        # print(50 * "-")
        # print(firstLine)


        # Process notIntersectingDucts First
        for points in sortPoints:
            for subPoint in points:
                toPoint = VisualizeGeometry.VisualizePoint(doc, subPoint)

        ductsValid = GetValidDucts(notIntersectingDucts,cutLength)







except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    # pass
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
