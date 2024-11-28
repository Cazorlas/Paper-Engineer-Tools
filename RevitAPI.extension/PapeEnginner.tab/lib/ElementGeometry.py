
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

class ElementGeometry:

    @staticmethod
    def GetElementSolid(element):
        '''
        Retrive the Solids of an Element.
        '''
        solids = []
        options = Options()
        geometry_element = element.get_Geometry(options)

        if geometry_element:
            for geometry_object in geometry_element:
                solid = geometry_object if isinstance(geometry_object, Solid) and geometry_object.Volume > 0 else None
                if solid:
                    solids.append(solid)
                else:
                    geometry_instance = geometry_object if isinstance(geometry_object, GeometryInstance) else None
                    if geometry_instance:
                        for instance_geometry_object in geometry_instance.GetInstanceGeometry():
                            instance_solid = instance_geometry_object if isinstance(instance_geometry_object, Solid) and instance_geometry_object.Volume > 0 else None
                            if instance_solid:
                                solids.append(instance_solid)

        return solids

    @staticmethod
    def GetFaceFromSolid(solid):
        '''
        Retrieves the Faces from a Solid.
        '''
        faces = [face for face in solid.Faces]
        return faces
    
    @staticmethod
    def UnionSolids(solids):
        union = None
        for solid in solids:
            if union == None:
                union = solid
            else:
                union = BooleanOperationsUtils.ExecuteBooleanOperation(union, solid,BooleanOperationsType.Union)
        return union
    
    @staticmethod
    def GetCentroidSolid(solid):
        return solid.ComputeCentroid()
    
    @staticmethod
    def GetBoundingBoxGeometry(geo):
        return geo.GetBoundingBox()

    @staticmethod
    def GetMinPoint(boundingbox):
        origin = boundingbox.Transform.Origin
        return boundingbox.Min + origin
    
    @staticmethod
    def GetMaxPoint(boundingbox):
        origin = boundingbox.Transform.Origin
        return boundingbox.Max + origin
    
    @staticmethod
    def GetBoundingBoxElement(ele):
        return ele.get_BoundingBox(None)

    @staticmethod
    def GetMinPointEle(boundingbox):
        return boundingbox.Min

    @staticmethod
    def GetMaxPointEle(boundingbox):
        return boundingbox.Max

    @staticmethod
    def GetCenterBoundingBox(boundingbox):
        minpoint = GetMinPoint(boundingbox)
        maxpoint = GetMaxPoint(boundingbox)
        centerpoint = (minpoint + maxpoint)/2
        return centerpoint
