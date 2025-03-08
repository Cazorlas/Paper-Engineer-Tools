
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

class VisualizeGeometry:
    
    @staticmethod
    def CreateDirectShape(doc, geometry_objects):
        direct_shape = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
        direct_shape.SetShape(geometry_objects)
        return direct_shape

    @staticmethod
    def VisualizePoint(doc, point):
        '''
        Visualize a Point by Generic Model.
        '''
        with Transaction(doc, "Visuallize Point") as t:
            t.Start()
            geometry_object = List[GeometryObject]([Point.Create(point)])
            VisualizeGeometry.CreateDirectShape(doc, geometry_object)
            t.Commit()

    @staticmethod
    def VisualizeLine(doc, start_point, end_point):
        '''
        Visualize a Line by Generic Model.
        '''
        with Transaction(doc, "Visuallize Line") as t:
            t.Start()
            line = List[GeometryObject]([Line.CreateBound(start_point, end_point)])
            VisualizeGeometry.CreateDirectShape(doc, line)
            t.Commit()

    @staticmethod
    def VisualizeSolid(doc, solids):
        '''
        Visualize a list of Solids by Generic Model.
        '''
        with Transaction(doc, "Visuallize Solid") as t:
            t.Start()
            geometry_objects = List[GeometryObject]([solid for solid in solids])
            newEle = VisualizeGeometry.CreateDirectShape(doc, geometry_objects)
            t.Commit()

        return newEle
    @staticmethod
    def VisualizeFace(doc, faces):
        '''
        Visualize a list of Faces by Generic Model.
        '''
        with Transaction(doc, "Visuallize Face") as t:
            t.Start()
            for face in faces:
                face_mesh = face.Triangulate()
                geometry_object = List[GeometryObject]([face_mesh])
                VisualizeGeometry.CreateDirectShape(doc, geometry_object)
            t.Commit()

    @staticmethod
    def VisualizeBoundingBoxFromSolid(doc, input_solid):
        '''
        Visualize a BoundingBox by Generic Model.
        '''
        with TransactionGroup(doc, "Visuallize Bounding Box") as tg:
            tg.Start()
            bbox = input_solid.GetBoundingBox()
            pt0 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
            pt1 = XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
            pt2 = XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
            pt3 = XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
            edges = [Line.CreateBound(pt0, pt1), Line.CreateBound(pt1, pt2), Line.CreateBound(pt2, pt3), Line.CreateBound(pt3, pt0)]
            height = bbox.Max.Z - bbox.Min.Z
            base_loop = CurveLoop.Create(List[Curve](edges))
            pre_transform_box = GeometryCreationUtilities.CreateExtrusionGeometry(List[CurveLoop]([base_loop]), XYZ.BasisZ, height)
            transform_box = SolidUtils.CreateTransformed(pre_transform_box, bbox.Transform)
            VisualizeGeometry.VisualizeSolid(doc, [transform_box])
            tg.Assimilate()


    @staticmethod
    def VisualizeBoundingBoxFromBoundingBox(doc, bbox):
        '''
        Visualize a BoundingBox by creating a Generic Model.
        '''
        with TransactionGroup(doc, "Visualize Bounding Box") as tg:
            tg.Start()

            # Define corner points of the bounding box
            pt0 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
            pt1 = XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
            pt2 = XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
            pt3 = XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)

            # Create the edges of the bounding box base
            edges = [Line.CreateBound(pt0, pt1), Line.CreateBound(pt1, pt2), Line.CreateBound(pt2, pt3), Line.CreateBound(pt3, pt0)]
            
            # Calculate the height of the bounding box and ensure it is positive
            height = max(bbox.Max.Z - bbox.Min.Z, 0.1)  # Set height to 0.1 if it is 0 or negative

            # Create the base loop and extrusion geometry
            base_loop = CurveLoop.Create(List[Curve](edges))
            pre_transform_box = GeometryCreationUtilities.CreateExtrusionGeometry(List[CurveLoop]([base_loop]), XYZ.BasisZ, height)
            
            # Apply transformation to align with the bounding box's transform
            transform_box = SolidUtils.CreateTransformed(pre_transform_box, bbox.Transform)
            
            # Visualize the transformed geometry
            VisualizeGeometry.VisualizeSolid(doc, [transform_box])
            
            tg.Assimilate()

    @staticmethod
    def VisualizePlane(doc, plane, width, height):
        '''
        Visualize a Plane as a rectangular face using DirectShape and Generic Model category.
        '''
        with Transaction(doc, "Visualize Plane") as t:
            t.Start()
            # Get plane properties
            origin = plane.Origin
            x_axis = plane.XVec
            y_axis = plane.YVec

            # Calculate rectangle corner points
            p1 = origin - (width / 2) * x_axis - (height / 2) * y_axis
            p2 = origin + (width / 2) * x_axis - (height / 2) * y_axis
            p3 = origin + (width / 2) * x_axis + (height / 2) * y_axis
            p4 = origin - (width / 2) * x_axis + (height / 2) * y_axis

            # Create the curve loop for the rectangle
            edges = [Line.CreateBound(p1, p2), Line.CreateBound(p2, p3), Line.CreateBound(p3, p4), Line.CreateBound(p4, p1)]
            curve_loop = CurveLoop.Create(List[Curve](edges))

            # Create the surface geometry
            plane_surface = GeometryCreationUtilities.CreateExtrusionGeometry([curve_loop], plane.Normal, 0.01)  # Small extrusion height

            # Create DirectShape for visualization
            VisualizeGeometry.CreateDirectShape(doc, [plane_surface])
            t.Commit()

