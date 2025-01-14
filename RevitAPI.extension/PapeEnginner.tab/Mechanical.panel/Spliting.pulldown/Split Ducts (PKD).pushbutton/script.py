#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr
import math
import System

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

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

    def __init__(self, categoryName, shapeType):
        self.category_name = categoryName
        self.shape_type = shapeType

    def AllowElement(self, e):
        if e.Category and e.Category.Name == self.category_name:
            if isinstance(e, Duct):
                duct_type = e.DuctType
                if duct_type and duct_type.Shape == self.shape_type:
                    return True
        return False

    def AllowReference(self, ref, point):
        return False


def CollectDuctAuto():
    ductsEles = FilteredElementCollector(doc, view.Id).OfClass(Duct).WhereElementIsNotElementType().ToElements()
    return ductsEles


def CollectDuctManual():
    collectorDucts = uidoc.Selection.PickObjects(ObjectType.Element,
                                                 SelectionFilter('Ducts', ConnectorProfileType.Rectangular),
                                                 'Select Ducts')
    ductsEles = [doc.GetElement(s.ElementId) for s in collectorDucts]
    return ductsEles


def flattenLv3(lst):
    return [i for sub_lst in lst for i in sub_lst]


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


def GetDuctTypeShape(shapeType, lstDucts):
    result = []

    for duct in lstDucts:
        ductShape = duct.DuctType.Shape
        if ductShape == shapeType:
            result.append(duct)

    return result


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


def GetVerticalDucts(lstDucts):
    verticalDucts = []
    otherDucts = []

    for duct in lstDucts:
        ductCurve = duct.Location.Curve
        lineDirection = ductCurve.Direction
        vectorNormalized = lineDirection.Normalize()
        zAxis = XYZ(0, 0, 1)

        # Tính dot product giữa vector ống và trục Z
        dotProduct = vectorNormalized.DotProduct(zAxis)

        # Nếu dot product gần bằng 1 hoặc -1, đây là ống đứng
        if abs(dotProduct - 1) < 1e-6 or abs(dotProduct + 1) < 1e-6:
            verticalDucts.append(duct)
        else:
            otherDucts.append(duct)

    return verticalDucts, otherDucts


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


def GetDuctUnionFamily(duct):
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
    """Get Connectors of Union Family (ft)"""
    UnionfamilyDoc = doc.EditFamily(unionFamily)
    familyConnector = GetConnectorsFromDocument(UnionfamilyDoc)
    connectorPoint1 = familyConnector[0].Origin
    connectorPoint2 = familyConnector[1].Origin
    distanceConnector = connectorPoint1.DistanceTo(connectorPoint2)
    # distanceConnector = round(connectorPoint1.DistanceTo(connectorPoint2) * 304.8)
    return distanceConnector


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


def ProcessData(Data):
    # Process Data
    intersectingDucts = []
    intersectingWalls = []
    intersectingPoints = []
    intersectingLines = []

    notIntersectingDucts = []

    # Hiển thị kết quả
    for data in Data:
        duct = data["Duct"]
        walls = data["Walls"]
        midpoints = data["Midpoints"]
        lines = data["Lines"]

        if walls:
            intersectingDucts.append(duct)
            intersectingWalls.append(walls)
            intersectingPoints.append(midpoints)
            intersectingLines.append(lines)
        else:
            notIntersectingDucts.append(duct)

    return intersectingDucts, intersectingWalls, intersectingPoints, intersectingLines, notIntersectingDucts


def AlignData(intersectingPoints, lstVector):
    # Align lstVector with intersectingPoints
    alignedVectors = []
    vectorIndex = 0
    for pointSublist in intersectingPoints:
        sublistVectors = []
        for _ in pointSublist:
            sublistVectors.append(lstVector[vectorIndex])
            vectorIndex += 1
        alignedVectors.append(sublistVectors)

    return alignedVectors


def SplitDuctByPoints(duct, pts):
    ele = []
    result = []
    with Transaction(doc, 'Break Curve') as t:
        t.Start()
        for pt in pts:
            try:
                ele.append(DB.Mechanical.MechanicalUtils.BreakCurve(doc, duct.Id, pt))
            except Exception as er:
                result.append(er)
        ele.append(duct.Id)
        result = [doc.GetElement(Id) for Id in ele]
        t.Commit()
    return result


def CurveAtSegmentLength(eles, distance, unionThickness):
    result = []
    for ele, thickness in zip(eles, unionThickness):
        # Get direction of element
        direct = ele.Location.Curve.Direction
        startPoint = ele.Location.Curve.GetEndPoint(0)
        # endPoint = ele.Location.Curve.GetEndPoint(1)

        # Divide length into pieces
        length = ele.LookupParameter('Length').AsDouble()  # ft
        section = int(length / (distance + (1 / 304.8)))
        lastSectionLength = length - (section * (distance / 304.8) + thickness)
        lstSub = []
        scale = float(0)

        for i in range(section):
            if i == 0:
                scale += float(distance) + float(thickness / 2)
            elif i > 0:
                scale += float(distance) + float(thickness)

            vectorDist = direct.Multiply(scale)
            newpoint = startPoint.Add(vectorDist)
            lstSub.append(newpoint)

        # Handle the last section if it's smaller than 150mm (0.492 ft)
        if lastSectionLength > 0:
            if lastSectionLength <= (150 / 304.8):  # 150mm in ft
                # Add the remaining length to the last segment
                if lstSub:
                    lstSub[-1] = lstSub[-1].Add(direct.Multiply(lastSectionLength))
            else:
                # Create a new segment for the remaining length
                scale += lastSectionLength
                vectorDist = direct.Multiply(scale)
                newpoint = startPoint.Add(vectorDist)
                lstSub.append(newpoint)

        result.append(lstSub)

    return result


# def CurveAtSegmentLength(eles, distance, unionThickness):
#     """
#     Chia đoạn ống thành các đoạn nhỏ với chiều dài cố định.
#     Đảm bảo không có đoạn ống thừa nào nhỏ hơn 250mm.
#
#     :param eles: Danh sách các đối tượng ống.
#     :param distance: Chiều dài mỗi đoạn (ft).
#     :param unionThickness: Độ dày của kết nối (ft).
#     :return: Danh sách các điểm chia đoạn cho từng ống.
#     """
#     result = []
#     minLength = 250 / 304.8  # 250mm in feet
#
#     for ele, thickness in zip(eles, unionThickness):
#         # Kiểm tra tính hợp lệ của ống
#         if ele is None or ele.Location is None or ele.Location.Curve is None:
#             continue
#
#         # Get direction of element
#         direct = ele.Location.Curve.Direction
#         startPoint = ele.Location.Curve.GetEndPoint(0)
#         endPoint = ele.Location.Curve.GetEndPoint(1)
#
#         # Lấy chiều dài ống
#         length_param = ele.LookupParameter('Length')
#         if length_param is None:
#             continue
#
#         length = length_param.AsDouble()  # Chiều dài ống (ft)
#         section = int(length / (distance + (1 / 304.8)))  # Số đoạn chia
#         lstSub = []
#         scale = float(0)
#
#         # Tính toán các điểm chia
#         for i in range(section):
#             if i == 0:
#                 scale += float(distance) + float(thickness / 2)
#             else:
#                 scale += float(distance) + float(thickness)
#
#             vectorDist = direct.Multiply(scale)
#             newpoint = startPoint.Add(vectorDist)
#             lstSub.append(newpoint)
#
#         # Xử lý đoạn thừa cuối cùng
#         if lstSub:
#             lastCutPoint = lstSub[-1]
#             remainingLength = lastCutPoint.DistanceTo(endPoint)
#
#             if remainingLength < minLength:  # Nếu đoạn thừa nhỏ hơn 250mm
#                 # Cộng đoạn thừa vào điểm chia cuối cùng
#                 lstSub[-1] = endPoint
#             else:
#                 # Nếu đoạn thừa lớn hơn hoặc bằng 250mm, thêm điểm cuối
#                 lstSub.append(endPoint)
#         else:
#             # Nếu không có điểm chia nào, thêm trực tiếp điểm cuối
#             lstSub.append(endPoint)
#
#         result.append(lstSub)
#
#     return result


"""----------------------MAIN CODE----------------------------"""
# Access the script's configuration
config = script.get_config()

try:
    nameLink, refLinkInstance, linkedTransform = CollectLinkData()
    nameLinkRemoveFirst = nameLink[1:]
    dictionary = dict(zip(nameLinkRemoveFirst, refLinkInstance))

    """----------------------------RUN FORMS----------------------------"""

    f = MainForm(nameLink)
    f.ShowDialog()

    # Retrieve previously saved settings (default to blank or zero if not found)
    previousStepLength = Config.get_option("StepLength", "0")  # Default: 0mm
    previousWallOffset = Config.get_option("WallOffset", "0")    # Default: 0mm
    previousLinkName = Config.get_option("LinkName", "No Link")  # Default: "No Link"

    # If 'OK' is clicked on the form
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # Get the desired length from the form input
        autoMode = f._radioButtonAuto.Checked
        manualMode = f._radioButtonManual.Checked
        planOption = f._radioButtonPlan.Checked
        verticalOption = f._radioButtonVertical.Checked
        allOption = f._radioButtonAll.Checked

        stepLength = float(f._textBoxStep.Text)  # mm
        cutLength = stepLength / 304.8  # ft
        offSetWall = float(f._textBoxWall.Text) / 304.8  # ft

        linkName = f._comboBoxLink.Text

        if linkName == "No Link":
            chooseRefLink = None

        else:
            chooseRefLink = dictionary.get(linkName)

        # Gọi hàm GetWalls để lấy danh sách tường
        walls = GetWalls(chooseRefLink)

        # Check if Auto Mode or Manual Mode is selected
        if autoMode:
            # Collect all ducts in the active view
            ductsCollector = CollectDuctAuto()
            ductsEles = GetDuctTypeShape(ConnectorProfileType.Rectangular, ductsCollector)
            verticalDucts, otherDucts = GetVerticalDucts(ductsEles)

            if planOption:
                ducts = otherDucts
            elif verticalOption:
                ducts = verticalDucts
            elif allOption:
                ducts = ductsEles
            else:
                ducts = ductsEles


        elif manualMode:
            # Manual duct selection
            ducts = CollectDuctManual()

        if len(ducts) == 0:
            TaskDialog.Show("Error", "There is no Selected Ducts")

        # Check intersections between walls and ducts
        intersectingData = GetIntersectingElements(chooseRefLink, walls, ducts)
        intersectingDucts, intersectingWalls, intersectingPoints, intersectingLines, notIntersectingDucts = ProcessData(
            intersectingData)

        with TransactionGroup(doc, "Split Ducts") as tg:
            tg.Start()
            # Process Ducts through the Walls first
            if len(intersectingDucts) > 0 and offSetWall > 0:
                intersectingDuctsValid = GetValidDucts(intersectingDucts, cutLength)
                ductEles = [doc.GetElement(duct.Id) for duct in intersectingDuctsValid]
                intersectingDuctUnion = [GetDuctUnionFamily(duct) for duct in ductEles]
                intersectingUnionThickness = [GetUnionThickness(union) for union in intersectingDuctUnion]
                offSet = offSetWall + (intersectingUnionThickness[0] / 2)

                # Process the Points
                lstVector = [l.Direction for lines in intersectingLines for l in lines]
                firstLine = [line[0] for line in intersectingLines]

                # Align lstVector with intersectingPoints
                alignedVectors = AlignData(intersectingPoints, lstVector)

                offsetPoints = GetOffSetPoints(offSet, alignedVectors, intersectingPoints)
                groupedOffsetPoints = GroupOffsetPoints(offsetPoints, intersectingPoints)
                sortPoints = SortPointByLineDirectionNested(firstLine, groupedOffsetPoints)

                # print(sortPoints)

                # THIS
                lst1Ducts = []
                lst2Ducts = []
                lstAllDucts = []

                for duct, subPoint in zip(intersectingDuctsValid, sortPoints):
                    lst1Ducts = SplitDuctByPoints(duct, subPoint)
                    lstAllDucts.append(lst1Ducts)
                    lst2Ducts = lst1Ducts[1:]

                    for ele1, ele2 in zip(lst1Ducts, lst2Ducts):
                        CreateFittings(ele1, ele2)

                lstDucts = notIntersectingDucts + flattenLv3(lstAllDucts)


            else:
                lstDucts = notIntersectingDucts

            ductsValid = GetValidDucts(lstDucts, cutLength)
            ductEles = [doc.GetElement(duct.Id) for duct in ductsValid]
            ductUnion = [GetDuctUnionFamily(duct) for duct in ductEles]
            unionThickness = [GetUnionThickness(union) for union in ductUnion]

            # Create a list of distances
            pts = CurveAtSegmentLength(ductEles, cutLength, unionThickness)

            lst1Ducts = []
            lst2Ducts = []

            for duct, subPoint in zip(ductsValid, pts):
                lst1Ducts = SplitDuctByPoints(duct, subPoint)
                lst2Ducts = lst1Ducts[1:]

                for ele1, ele2 in zip(lst1Ducts, lst2Ducts):
                    CreateFittings(ele1, ele2)

            tg.Assimilate()


except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
