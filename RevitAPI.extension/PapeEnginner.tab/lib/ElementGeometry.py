
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
