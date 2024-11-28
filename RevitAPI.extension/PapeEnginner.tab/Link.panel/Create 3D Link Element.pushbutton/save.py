#Inspired by https://forum.dynamobim.com/t/zoom-to-selected-element-in-a-linked-document/61279/6

import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

def SumBoxes(boxes):
	minx = min([b.Min.X for b in boxes])
	miny = min([b.Min.Y for b in boxes])
	minz = min([b.Min.Z for b in boxes])
	maxx = max([b.Max.X for b in boxes])
	maxy = max([b.Max.Y for b in boxes])
	maxz = max([b.Max.Z for b in boxes])
	bb = BoundingBoxXYZ()
	bb.Min = XYZ(minx,miny,minz)
	bb.Max = XYZ(maxx,maxy,maxz)
	return bb

class CustomISelectionFilter(ISelectionFilter):
	def AllowElement(self, e):
		return True

	def AllowReference(self, refer, point):
		rvtlnkInstance = doc.GetElement(refer)
		docLink = rvtlnkInstance.GetLinkDocument()
		elemLink = docLink.GetElement(refer.LinkedElementId)
		if elemLink.Category.CategoryType == CategoryType.Model and elemLink.Category.Id.IntegerValue != BuiltInCategory.OST_DetailComponents.value__ and elemLink.Category.Id.IntegerValue != BuiltInCategory.OST_RasterImages.value__:
			return True
		else:
			return False

#Get 3D View ViewFamilyType
viewType = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements().Find(lambda x : x.ViewFamily == ViewFamily.ThreeDimensional)

bbx,elemInLinks=[],[]
TaskDialog.Show("Selection", "Select the linked elements and press Finish")
reflnk = uidoc.Selection.PickObjects(ObjectType.LinkedElement, CustomISelectionFilter(), "Select linked elements")
for ref in reflnk :
	lnkinst=doc.GetElement(ref)
	tfLnk = lnkinst.GetTotalTransform()
	doclnk =  lnkinst.GetLinkDocument()
	elemInLink = doclnk.GetElement(ref.LinkedElementId)
	elemInLinks.append(elemInLink)
	box = elemInLink.get_BoundingBox(None)
	box.Min = tfLnk.OfPoint(box.Min)
	box.Max = tfLnk.OfPoint(box.Max)
	#box.Transform = tfLnk
	bbx.append(box)
	sumBox = SumBoxes(bbx)

TransactionManager.Instance.EnsureInTransaction(doc)
if doc.ActiveView.ViewType == ViewType.ThreeD:
	view = doc.ActiveView
else:
	view = View3D.CreateIsometric(doc, viewType.Id)
view.SetSectionBox(sumBox)

TransactionManager.Instance.TransactionTaskDone()

TransactionManager.Instance.ForceCloseTransaction()
#Impossible to set the uidoc.ActiveView in Revit’s Idling event since Dynamo operates inside this event
#uidoc.ActiveView = view
uidoc.RequestViewChange(view)
uidoc.RefreshActiveView()
#Zoom to the linked elements
try :
	uiviews = uidoc.GetOpenUIViews()
	uiview = [x for x in uiviews if x.ViewId == view.Id][0]
	uiview.ZoomAndCenterRectangle(sumBox.Min, sumBox.Max)
except : pass

if len(elemInLinks)>1: OUT = view, elemInLinks, lnkinst
else:OUT = view, elemInLinks[0], lnkinst