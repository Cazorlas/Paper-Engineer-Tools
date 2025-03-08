import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

class RevitUtils:

    @staticmethod
    def ClosestConnectors(element1, element2):
        '''
        Get two closest connectors from two elements.
        '''

        conn1 = RevitUtils.GetElementConnectors(element1)
        conn2 = RevitUtils.GetElementConnectors(element2)
        
        dist = 100000000
        connset = None
        for c in conn1:
            for d in conn2:
                conndist = c.Origin.DistanceTo(d.Origin)
                if conndist < dist:
                    dist = conndist
                    connset = [c,d]
        return connset
    
    @staticmethod
    def GetElementConnectors(element):
        '''
        Get all connectors of an element.
        '''
        try:
            connectors = element.MEPModel.ConnectorManager.Connectors
        except:
            try:
                connectors = element.ConnectorManager.Connectors
            except:			
                connectors = []
        return [x for x in connectors]
    
    @staticmethod
    def PullPointOntoPlane(point, plane):
        '''
        Return a point which is projected onto a plane.
        '''
        # Get the normal vector and origin of the plane
        normalVector = plane.Normal
        planeOrigin = plane.Origin

        # Calculate the projected points using list comprehension
        pullPoint = point.Add(normalVector.Multiply(normalVector.DotProduct(planeOrigin) - normalVector.DotProduct(point)))

        return pullPoint
    
    @staticmethod
    def GetEditableFamily(doc):
        '''
        Return all the editable families in the given document.
        '''
        #Retrieve all families that are not system families in current doc
        allFamilies = FilteredElementCollector(doc).OfClass(Family).ToElements()

        #Filter the editable families and resultput result
        editableFamilies = []
        for i in allFamilies:
            if (i.IsEditable):
                editableFamilies.append(i)
        
        return editableFamilies

    @staticmethod
    def GetFamilySymbolFromFamily(doc,family):
        '''
        Return all the family types of a family in a given document.
        '''
        IdHashSet = family.GetFamilySymbolIds()
        IdLst = list(IdHashSet)
        return [doc.GetElement(Id) for Id in IdLst]
