#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clr
# clr.AddReference('RevitAPI')
# clr.AddReference('RevitAPIUI')


from System.Collections.Generic import List

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

# Prepare document and other variables
# doc = __revit__.ActiveUIDocument.Document
# view = doc.ActiveView
# uidoc = __revit__.ActiveUIDocument
# app = __revit__.Application
# DB = Autodesk.Revit.DB
# unit = doc.GetUnits()
# version = int(app.VersionNumber)
""" ----------------------MAIN CODE----------------------------"""
class Visualize:

    @staticmethod
    def CreateDirectShape(doc, geometryObjects, builtInCategory=BuiltInCategory.OST_GenericModel):

        # Tạo DirectShape từ Document và category
        directShape = DirectShape.CreateElement(doc, ElementId(builtInCategory))

        # Thiết lập hình dạng cho DirectShape
        directShape.SetShape(geometryObjects)
        return directShape

    @staticmethod
    def VisualizePoint(doc,points):
        # Giả sử 'points' là danh sách các đối tượng GeometryObject (có thể là các điểm dạng XYZ đã được chuyển đổi thành GeometryObject nếu cần)
        with Transaction(doc, "Create Points") as t:
            t.Start()
            # Ở đây, chúng ta gọi CreateDirectShape để tạo DirectShape từ danh sách points
            visualizePoint = Visualize.CreateDirectShape(doc, List[GeometryObject]([Point.Create(points)]))
            t.Commit()

        return visualizePoint

    @staticmethod
    def VisualizeLine(doc,vector,origin = XYZ.Zero):

        endPoint = origin + vector

        with Transaction(doc, "Create Line") as t:
            t.Start()
            line = Line.CreateBound(origin, endPoint)

            visualizeLine =  Visualize.CreateDirectShape(doc, List[GeometryObject]([line]))
            t.Commit()

        return visualizeLine

    @staticmethod
    def VisualizePlane(doc, plane, width=5.0, height=5.0, extrusionDepth=0.1):
        """
        Hiển thị một mặt phẳng dựa trên đối tượng Plane.

        :param doc: Document của Revit.
        :param plane: Đối tượng Plane từ Revit (mặt phẳng cần visualize).
        :param width: Chiều rộng mặt phẳng.
        :param height: Chiều cao mặt phẳng.
        :param extrusionDepth: Độ dày của mặt phẳng (đùn theo normal của plane).
        """

        with Transaction(doc, "Create Plane") as t:
            t.Start()

            # Lấy gốc tọa độ của plane
            origin = plane.Origin
            xVec = plane.XVec.Normalize() * width  # Vector X có độ dài width
            yVec = plane.YVec.Normalize() * height  # Vector Y có độ dài height
            zVec = plane.Normal.Normalize() * extrusionDepth  # Vector Z theo normal

            # Xác định 4 điểm của hình chữ nhật trên plane
            p1 = origin
            p2 = origin + xVec
            p3 = origin + xVec + yVec
            p4 = origin + yVec

            # Tạo biên dạng (CurveLoop)
            loop = CurveLoop()
            loop.Append(Line.CreateBound(p1, p2))
            loop.Append(Line.CreateBound(p2, p3))
            loop.Append(Line.CreateBound(p3, p4))
            loop.Append(Line.CreateBound(p4, p1))

            # Tạo Solid bằng cách Extrude hình chữ nhật theo hướng của plane.Normal
            solid = GeometryCreationUtilities.CreateExtrusionGeometry([loop], zVec, extrusionDepth)

            # Hiển thị mặt phẳng trong Revit
            visualizePlane = Visualize.CreateDirectShape(doc, List[GeometryObject]([solid]))

            t.Commit()

        return visualizePlane
