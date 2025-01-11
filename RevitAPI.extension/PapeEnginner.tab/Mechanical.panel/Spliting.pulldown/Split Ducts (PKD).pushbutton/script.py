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


def GetValidDuct(ducts, stepLength):
    validDucts = []

    for duct in ducts:
        family = duct.LookupParameter('Family').AsValueString()
        duct_length_check = duct.LookupParameter('Length').AsDouble()  # ft
        if duct_length_check > stepLength:
            validDucts.append(duct)

    return validDucts


def CollectLinkData():
    """
    Collect all required data about Revit links in the model.
    """
    refLinkInstance = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    linkType = [doc.GetElement(ref.GetTypeId()) for ref in refLinkInstance]
    # docLink = [ref.GetLinkDocument() for ref in refLinkInstance]

    nameLink = ["No Link"] + [link.LookupParameter("Type Name").AsString() for link in linkType] if linkType else [
        "There is no Link Model"]

    return nameLink, refLinkInstance


def GetWalls(refLinkInstance, linkName):
    """
    Collect all Wall Instances from the active view or a linked model.
    :param refLinkInstance: List of LinkInstance elements in the model.
    :param linkName: Selected name of the link from the ComboBox.
    :return: List of Wall Instances.
    """
    # linkType = [doc.GetElement(ref.GetTypeId()) for ref in refLinkInstance]

    if linkName == "There is no Link Model" or linkName == "No Link":
        # Collect walls from the active view in the current document
        refwalls = FilteredElementCollector(doc, view.Id).OfCategory(
            BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
        walls = [doc.GetElement(wall.Id) for wall in refwalls]
    else:
        # Check if the selected link exists in the document

        for refLink in refLinkInstance:
            linkType = doc.GetElement(refLink.GetTypeId())
            linkTypeName = linkType.LookupParameter("Type Name").AsString()

            # if not linkedDoc:
            #     raise Exception("Linked document '{}' is not loaded.".format(linkName))

            if linkTypeName == linkName:
                linkedDoc = refLink.GetLinkDocument()
                # Thu thập tường từ view hiện tại trong tài liệu liên kết
                walls = FilteredElementCollector(linkedDoc, view.Id).OfCategory(
                    BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
                # walls = [linkedDoc.GetElement(wall.LinkedElementId) for wall in refWalls]
                break

    return walls


def GetSolidFromElement(element):
    """
    Lấy Solid từ một phần tử Revit.
    :param element: Phần tử Revit.
    :return: Solid của phần tử hoặc None nếu không có.
    """
    options = Options()
    geometry = element.get_Geometry(options)
    if geometry is None:
        return None

    for object in geometry:
        if isinstance(object, Solid) and object.Volume > 0:
            return object

    return None


def GetIntersectingElements(refLinkInstance, lstA, lstB):
    """
    Kiểm tra giao cắt giữa hai danh sách phần tử.
    :param refLinkInstance: Đối tượng liên kết RevitLinkInstance (nếu có).
    :param lstA: Danh sách các tường (walls).
    :param lstB: Danh sách các ống gió (ducts).
    :return: Danh sách các phần tử từ lstA giao cắt với lstB.
    """
    intersectingElements = []

    # Xác định tài liệu và transform (nếu là liên kết)
    if refLinkInstance:
        document = refLinkInstance.GetLinkDocument()
        transform = refLinkInstance.GetTransform()
    else:
        document = doc
        transform = Transform.Identity

    for eleA in lstA:
        # Lấy Solid từ eleA
        solidA = GetSolidFromElement(eleA)
        if not solidA:
            continue

        # Áp dụng transform nếu là liên kết
        solid = SolidUtils.CreateTransformed(solidA, transform.Inverse) if refLinkInstance else solidA

        # Tạo bộ lọc giao cắt Solid
        solidFilter = ElementIntersectsSolidFilter(solid)

        # Thu thập các phần tử giao cắt với solidA
        intersectingCollector = FilteredElementCollector(document).WhereElementIsNotElementType().WherePasses(
            solidFilter).ToElements()

        # Kiểm tra nếu các phần tử trong lstB nằm trong danh sách giao cắt
        for eleB in intersectingCollector:
            if eleB.Id in [b.Id for b in lstB]:
                intersectingElements.append(eleA)
                break  # Dừng kiểm tra nếu tìm thấy phần tử giao cắt

    return intersectingElements


    # for eleA in lstA:
    #     transform = eleA.GetTransform()
    #
    #     filter = ElementIntersectsElementFilter(eleA)
    #     intersectingCollector = FilteredElementCollector(document, view.Id).WhereElementIsNotElementType().WherePasses(
    #         filter).ToElements()
    #
    #     # Kiểm tra phần tử trong lstB
    #     for ele in intersectingCollector:
    #         if ele.Id in [b.Id for b in lstB]:
    #             intersectingElements.append(eleA)
    #             break  # Dừng kiểm tra nếu đã tìm thấy giao cắt
    #
    # # print(intersectingCollector)
    # return intersectingElements


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

    # abc = {'Option 1': 10.0, 'Option 2': 20.0}
    #
    # # Khởi tạo các thành phần của Form
    # components = [Label('Pick Style:'),
    #               Separator(),  # Dấu phân cách làm tiêu đề
    #               # ComboBox('combobox1', abc),  # Hộp chọn với các tùy chọn
    #               Separator(),  # Dấu phân cách
    #               ComboBox('textbox1', abc),  # Hộp chọn thay thế TextBox
    #               CheckBox('checkbox1', 'Check this'),  # Ô chọn (Checkbox)
    #               Separator(),  # Dấu ngăn cách
    #               Button('Select')  # Nút bấm
    #               ]
    #
    # # Tạo và hiển thị FlexForm
    # form = FlexForm('My Custom Form', components)
    # result = form.show()
    #
    # # Xử lý kết quả từ Form
    # if result:
    #     selected_option = result.get('combobox1')
    #     entered_text = result.get('textbox1')
    #     checkbox_state = result.get('checkbox1')
    # else:
    #     pass

    nameLink, refLinkInstance = CollectLinkData()
    # print(transform)

    dictionary = dict(zip(nameLink, refLinkInstance))
    """----------------------------RUN FORMS----------------------------"""

    f = MainForm(nameLink)
    f.ShowDialog()

    # If 'OK' is clicked on the form
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # Get the desired length from the form input
        autoMode = f._radioButtonAuto.Checked
        manualMode = f._radioButtonManual.Checked
        stepLength = float(f._textBoxStep.Text)  # mm
        stepWall = float(f._textBoxWall.Text)
        linkName = f._comboBoxLink.Text

        # Gọi hàm GetWalls để lấy danh sách tường
        walls = GetWalls(refLinkInstance, linkName)

        if refLinkInstance:
            chooseRefLink = dictionary.get("{}".format(linkName))
        else:
            chooseRefLink = null

        # print(chooseDocument)

        # print(walls)

        # Check if Auto Mode or Manual Mode is selected
        if autoMode:
            # Collect all ducts in the active view
            collectorDucts = CollectDuctAuto()
            ductsEles = [doc.GetElement(s.Id) for s in collectorDucts]
            intersectingWalls = GetIntersectingElements(chooseRefLink, walls, ductsEles)
            print(intersectingWalls)
        elif manualMode:
            # Manual duct selection
            collectorDucts = CollectDuctManual()
            ductsEles = [doc.GetElement(s.ElementId) for s in collectorDucts]
            # Check intersections between walls and ducts
            intersectingWalls = GetIntersectingElements(chooseRefLink, walls, ductsEles)
            print(intersectingWalls)




except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    # pass
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
