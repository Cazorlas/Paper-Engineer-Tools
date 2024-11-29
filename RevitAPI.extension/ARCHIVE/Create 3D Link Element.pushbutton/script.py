#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clr 
from pyrevit import forms
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *




# Import Minh Tran library
from ModelSelection import *
from VisuallizeGeometry import *
from RevitUtils import *
from ElementGeometry import *

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB

#-----------------------------Function------------------------------------------
def GetLinkDoc():
    linkInstances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    linkDoc = []
    linkName = []
    for i in linkInstances:
        linkDoc.append(i.GetLinkDocument())
        linkName.append(i.Name)
    return linkDoc,linkName,linkInstances

def Flatten_LV3(lst):
    return [item for sublst in lst for item in sublst]

def Create3DView (threeDViewType, boundingBox, viewName):
    newIsometric = DB.View3D.CreateIsometric(doc,threeDViewType.Id)
    newIsometric.SetSectionBox(boundingBox)
    nameParameter = newIsometric.LookupParameter('View Name')
    nameParameter.Set(viewName)


#-----------------------------Function------------------------------------------
# Get 3D view typee
allViewTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType)
threeDViewTypes = []
for viewType in allViewTypes:
    if viewType.ViewFamily == ViewFamily.ThreeDimensional:
        threeDViewTypes.append(viewType)

# Select link file
allLinkDoc = GetLinkDoc()
allLinkDocDict = dict(zip(allLinkDoc[1],allLinkDoc[0]))
selectedLinkModelName = forms.SelectFromList.show({'Link Models' : sorted(allLinkDocDict)},
                                multiselect=False,
                                group_selector_title='Link Model Sets',
                                button_name='Select a Link Model')
if not selectedLinkModelName:
    TaskDialog.Show('No Linked Model Selected. Please Select Again.',exit = True)


for ind,name in enumerate(allLinkDoc[1]):
    if selectedLinkModelName == name:
        linkedRvtInstance = allLinkDoc[2][ind]
        linkedDoc = allLinkDoc[0][ind]
        break

# Input link ID
linkID = forms.ask_for_string(
    default='Linked Element ID',
    prompt='Enter a linked element ID',
    title=None
)
lstlinkIDs = [int(Id) for Id in linkID.split(",")]
linkedElements = [linkedDoc.GetElement(ElementId(Id)) for Id in lstlinkIDs]
linkedSolids = Flatten_LV3([ElementGeometry.GetElementSolid(ele) for ele in linkedElements])
solidUnion = ElementGeometry.UnionSolids(linkedSolids)
solidUnionBoundingBox = ElementGeometry.GetBoundingBoxGeometry(solidUnion)


# Đoạn transform này chỉ áp dụng cho trường hợp file link
# Nếu dùng cho trường hợp In Model của anh bạn thì đưa trục tiếp solidUnionBoundingBox vào phần Execution ở dưới
# Get link transform
minPoint = ElementGeometry.GetMinPoint(solidUnionBoundingBox)
maxPoint = ElementGeometry.GetMaxPoint(solidUnionBoundingBox)
linkedTransform = linkedRvtInstance.GetTransform()
transformMinPoint = linkedTransform.OfPoint(minPoint)
transformMaxPoint = linkedTransform.OfPoint(maxPoint)

# Create new bounding box after transforming 
transformBoundingBox = BoundingBoxXYZ()
transformBoundingBox.Min = transformMinPoint # Set new min point
transformBoundingBox.Max = transformMaxPoint # Set new max point


# VisuallizeGeometry.VisuallizePoint(doc , transformMinPoint)
# VisuallizeGeometry.VisuallizePoint(doc , transformMaxPoint)

#-----------------------------Execution-----------------------------------------
with Transaction(doc,"Create 3D View") as t:
    t.Start()

    # Nếu muốn tạo view 3D mới thì bỏ comment ở dòng này
    # Create3DView(threeDViewTypes[0],transformBoundingBox,"Test")

    # Nếu chỉ muốn set section box cho view 3D hiện tại
    view.SetSectionBox(transformBoundingBox)
    t.Commit()

