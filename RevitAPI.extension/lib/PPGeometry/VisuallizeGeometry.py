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
class Visuallize:

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
            visualizePoint = Visuallize.CreateDirectShape(doc,List[GeometryObject]([Point.Create(points)]))
            t.Commit()

        return visualizePoint

    @staticmethod
    def VisualizeLine(doc,vector,origin = XYZ.Zero):

        endPoint = origin + vector

        with Transaction(doc, "Create Line") as t:
            t.Start()
            line = Line.CreateBound(origin, endPoint)

            visualizeLine =  Visuallize.CreateDirectShape(doc, List[GeometryObject]([line]))
            t.Commit()

        return visualizeLine
