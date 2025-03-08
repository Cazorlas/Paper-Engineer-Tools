
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
        '''
        Join the list of solids into one solid.
        '''
        union = None
        for solid in solids:
            if union == None:
                union = solid
            else:
                union = BooleanOperationsUtils.ExecuteBooleanOperation(union, solid,BooleanOperationsType.Union)
        return union
    
    @staticmethod
    def GetCentroidSolid(solid):
        '''
        Get the centroid of a solid.
        '''
        return solid.ComputeCentroid()
    
    @staticmethod
    def GetBoundingBoxGeometry(geo):
        '''
        Get the bounding box of a solid.
        If you want exact result, this method is not recommended because it returns results with small tolerances.
        You should use GetBoundingBoxElement instead.
        '''
        return geo.GetBoundingBox()

    @staticmethod
    def GetMinPoint(boundingbox):
        '''
        Get the min point of a solid's bounding box.
        '''
        origin = boundingbox.Transform.Origin
        return boundingbox.Min + origin
    
    @staticmethod
    def GetMaxPoint(boundingbox):
        '''
        Get the max point of a solid's bounding box.
        '''
        origin = boundingbox.Transform.Origin
        return boundingbox.Max + origin
    
    @staticmethod
    def GetBoundingBoxElement(ele):
        '''
        Get bounding box of an elemment
        '''
        return ele.get_BoundingBox(None)

    @staticmethod
    def GetMinPointEle(boundingbox):
        '''
        Get the min point of a element's bounding box.
        '''
        return boundingbox.Min

    @staticmethod
    def GetMaxPointEle(boundingbox):
        '''
        Get the max point of a element's bounding box.
        '''
        return boundingbox.Max

    @staticmethod
    def GetCenterBoundingBox(boundingbox):
        '''
        Get the center point of a element's bounding box.
        '''
        minpoint = ElementGeometry.GetMinPoint(boundingbox)
        maxpoint = ElementGeometry.GetMaxPoint(boundingbox)
        centerpoint = (minpoint + maxpoint)/2
        return centerpoint

    @staticmethod
    def SumBoundingBoxes(boundingBoxes, offset):
        """
        Calculate the sum of BoundingBoxXYZ.
        Parameters:
        - boundingBoxes: List of BoundingBoxXYZ.
        Returns:
        - BoundingBoxXYZ that contains the sum of all input BoundingBoxes.
        """

        minX = min([b.Min.X for b in boundingBoxes]) - offset
        minY = min([b.Min.Y for b in boundingBoxes]) - offset
        minZ = min([b.Min.Z for b in boundingBoxes]) - offset
        maxX = max([b.Max.X for b in boundingBoxes]) + offset
        maxY = max([b.Max.Y for b in boundingBoxes]) + offset
        maxZ = max([b.Max.Z for b in boundingBoxes]) + offset
        bb = BoundingBoxXYZ()
        bb.Min = XYZ(minX, minY, minZ)
        bb.Max = XYZ(maxX, maxY, maxZ)
        return bb
    
    @staticmethod
    def AngleAboutAxis(vector1,vector2,axis):
        '''
        Get the angle between vector 1 and vector 2 around a axis.
        '''
        angle = vector1.AngleOnPlaneTo(vector2,axis)
        return angle
    
    @staticmethod
    def RotateGeometry(geometry, origin, axis, angle):
        '''
        Get a geometry around a point and a axis with an angle.
        '''
        rotationTransform = Transform.CreateRotationAtPoint(axis, angle, origin)

        transformedGeoObject = SolidUtils.CreateTransformed(geometry,rotationTransform)

        return transformedGeoObject